from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=20)

    def get_absolute_url(self):
        return "/categories/{}".format(self.id)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=120)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return "/posts/{}".format(self.id)

    def __str__(self):
        return "{} - {}".format(self.id, self.title)

