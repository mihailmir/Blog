from blog import app
from .forms import CommentsForm, ChildCommentsForm


@app.task(bind=True, max_retries=5)
def add_comments(self, user_id, **kwargs):
    form = CommentsForm
    if kwargs.get('parent'):
        form = ChildCommentsForm

    form = form(kwargs)
    if form.is_valid():
        form.save(commit=True, user_id=user_id)
