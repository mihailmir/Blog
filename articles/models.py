from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from treebeard.mp_tree import MP_Node


class Articles(models.Model):
    title = models.CharField(db_index=True, max_length=50)
    article_body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('view_article', args=[self.id])


class Comments(MP_Node):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    comment_body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
