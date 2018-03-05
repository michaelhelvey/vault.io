from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404, render
from django import http
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from web.models import Category, Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def search(request):
    search_query = request.POST['search_query']
    search_result = Post.objects.filter(content__search=search_query)
    return render(request, 'search.html', {
        'search_results': search_result,
        'search_query': search_query
    })


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self):
        return {
            'categories': Category.objects.order_by('title'),
            'recent_posts': Post.objects.order_by('-createdAt')[:10]
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
            'posts': Post.objects.filter(category=self.category).order_by('-createdAt')
        }


class PostView(DetailView):
    model = Post
    template_name = "post.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'content']
    template_name = 'post_form.html'
    success_url = "/posts/{id}/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()  
        return http.HttpResponseRedirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model = Post
    fields = ['title', 'category', 'content']
    template_name = 'post_update_form.html'

    def test_func(self):
        return Post.objects.get(pk=self.kwargs['pk']).user.id == self.request.user.id

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    template_name = "post_delete_form.html"

    def get_success_url(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return '/categories/{}/'.format(post.category.id)

    def test_func(self):
        return Post.objects.get(pk=self.kwargs['pk']).user.id == self.request.user.id