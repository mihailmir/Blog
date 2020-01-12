from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, View
from .forms import ArticlesForm, CommentsForm
from .models import Articles, Comments
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin
from django.utils.functional import cached_property
from .tasks import add_comments


class CustomPaginator(Paginator):
    def __init__(self, object_list, per_page, orphans=0,
                 allow_empty_first_page=True):
        super().__init__(object_list, per_page, orphans=orphans,
                 allow_empty_first_page=allow_empty_first_page)
        self.paginate()

    def paginate(self):
        result = {}
        temp = []
        page = 1
        for c in self.object_list:
            temp.extend(Comments.get_tree(c))
            if len(temp) >= self.per_page:
                result[page] = temp
                page += 1
                temp = []
        if temp:
            result[page] = temp
        self.object_list = result

    def page(self, number):
        return self._get_page(self.object_list.get(number, []), number, self)

    @cached_property
    def num_pages(self):
        return len(self.object_list)


class ArticlesList(ListView):
    model = Articles
    template_name = 'articles_list.html'
    context_object_name = 'articles'


class ArticleView(DetailView):
    model = Articles
    secondary_model = Comments
    template_name = 'articles_view.html'
    context_object_name = 'article'
    extra_context = {}

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.extra_context['comments_form'] = CommentsForm
        return super().get(self, request, *args, **kwargs)


# ajax
class CommentsView(MultipleObjectMixin, View):
    model = Comments
    paginator_class = CustomPaginator
    context_object_name = 'comments'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        article_id = request.GET.get('article_id')
        root_comments = self.model.objects.filter(article_id=article_id, depth=1).order_by('create_date')
        context = self.get_context_data(object_list=root_comments)
        return render(request, 'embed/comments_block.html', context=context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ArticlesForm
    model = Articles
    template_name = 'articles_form.html'
    initial = {}

    def post(self, request, *args, **kwargs):
        self.initial.update({'user': request.user})
        return super().post(self, request, *args, **kwargs)


class ArticleAddCommentView(LoginRequiredMixin, View):
    raise_exception = True
    form = CommentsForm

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'embed/comments_form.html',
            context={
                'comments_form': self.form(),
                'article_id': request.GET.get('article_id'),
                'parent_id': request.GET.get('comment_id')
            }
        )

    def post(self, request, *args, **kwargs):
        add_comments.apply_async(args=[request.user.id],  kwargs=request.POST, countdown=10)
        return redirect('view_article', request.POST.get('article'))
