from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, View
from .forms import ArticlesForm, CommentsForm, ChildCommentsForm
from .models import Articles, Comments
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render


# Create your views here.


# class AjaxableResponseMixin:
#     """
#     Mixin to add AJAX support to a form.
#     Must be used with an object-based FormView (e.g. CreateView)
#     """
#     def form_invalid(self, form):
#         response = super().form_invalid(form)
#         if self.request.is_ajax():
#             return JsonResponse(form.errors, status=400)
#         else:
#             return response
#
#     def form_valid(self, form):
#         # We make sure to call the parent's form_valid() method because
#         # it might do some processing (in the case of CreateView, it will
#         # call form.save() for example).
#         response = super().form_valid(form)
#         if self.request.is_ajax():
#             data = {
#                 'comment': form.cleaned_data.get('comment_body')
#             }
#             return JsonResponse(data)
#         else:
#             return response


class ArticlesList(ListView):
    model = Articles
    template_name = 'articles_list.html'
    context_object_name = 'articles'
    # paginate_by = 5
    # extra_context = {'nav_range': 3}


class ArticleView(DetailView):
    model = Articles
    secondary_model = Comments
    template_name = 'articles_view.html'
    context_object_name = 'article'
    extra_context = {}
    initial = {}

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs.get(self.pk_url_kwarg)
        comment = self.secondary_model.objects.filter(article_id=article_id, depth=1).order_by('-create_date')

        self.extra_context['comments'] = []
        self.extra_context['article_id'] = article_id

        if comment.exists():
            self.extra_context['comments'] = [self.secondary_model.get_tree(parent=c) for c in comment]

        if self.request.user.is_authenticated:
            self.extra_context['comments_form'] = CommentsForm
        return super().get(self, request, *args, **kwargs)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ArticlesForm
    model = Articles
    template_name = 'articles_form.html'
    initial = {}

    def post(self, request, *args, **kwargs):
        self.initial.update({'user': request.user})
        return super().post(self, request, *args, **kwargs)


class ArticleAddCommentView(View):
    raise_exception = True
    form = CommentsForm
    initial = {}

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'comments_form.html',
            context={
                'comments_form': CommentsForm(),
                'article_id': request.GET.get('article_id'),
                'parent_id': request.GET.get('comment_id')
            }
        )

    def post(self, request, *args, **kwargs):
        self.form = CommentsForm
        if request.POST.get('parent'):
            self.form = ChildCommentsForm

        self.form = self.form(request.POST)
        if self.form.is_valid():
            self.form.save(commit=True, user=request.user)

        return redirect('view_article', request.POST.get('article'))





