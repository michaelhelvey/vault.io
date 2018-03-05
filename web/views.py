from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from web.models import Category, Post


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self):
        return {
            'categories': Category.objects.order_by('title'),
            'recent_posts': Post.objects.order_by('createdAt')
        }


class ProfileView(TemplateView):
    template_name = "profile.html"


class AboutView(TemplateView):
    template_name = "about.html"


class CategoryView(ListView):
    model = Post
    template_name = "category.html"

    def get_context_data(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return {
            'categories': Category.objects.order_by('title'),
            'current_category': self.category,
            'posts': Post.objects.filter(category=self.category)
        }


class PostView(DetailView):
    model = Post
    template_name = "post.html"

