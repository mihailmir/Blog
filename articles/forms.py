from django.forms import ModelForm, TextInput, Textarea, IntegerField
from .models import Articles, Comments
from django.core.exceptions import ValidationError


def validate_entity(entity):
    def validate(value):
        if not entity.objects.filter(pk=value).exists():
            raise ValidationError('{} does not exist.'.format(entity.__name__))
    return validate


class ArticlesForm(ModelForm):

    class Meta:
        model = Articles
        fields = ['title', 'article_body']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'article_body': Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        inst = super().save(commit=False)
        inst.author = self.initial.pop('user')
        if commit:
            inst.save()

        return inst


class CommentsForm(ModelForm):
    article = IntegerField(validators=[validate_entity(Articles)])

    class Meta:
        model = Comments
        fields = ['comment_body']
        widgets = {
            'comment_body': Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True, user_id=None):

        self.instance.__class__.add_root(
            article_id=self.cleaned_data.get('article'),
            author_id=user_id,
            comment_body=self.cleaned_data.get('comment_body')
        )
        return self.instance


class ChildCommentsForm(CommentsForm):
    parent = IntegerField(validators=[validate_entity(Comments)])

    def save(self, commit=True, user_id=None):

        article = self.instance.__class__.objects.get(pk=self.cleaned_data.get('parent'))
        self.instance.__class__.add_child(
            article,
            article_id=self.cleaned_data.get('article'),
            author_id=user_id,
            comment_body=self.cleaned_data.get('comment_body')
        )
        return self.instance
