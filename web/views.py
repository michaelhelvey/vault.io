from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django import http
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from web.models import Category, Post, UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tinymce.widgets import TinyMCE
from django import forms

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

    def get_context_data(self):
        return {
            user: self.request.user
        }


class AboutView(TemplateView):
    template_name = "about.html"


class CategoryView(ListView):
    model = Post
    template_name = "category.html"
    context_object_name = "posts_list"
    paginate_by = 20

    def get_queryset(self):
        queryset = Post.objects.filter(category_id=self.kwargs['category_id'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        context['categories'] = Category.objects.order_by('title')
        context['current_category'] = self.category
        return context



class PostView(DetailView):
    model = Post
    template_name = "post.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'content']
    template_name = 'post_form.html'
    success_url = "/posts/{id}/"

    def get_form(self):
        form = super().get_form()
        form.fields['content'] = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()  
        return http.HttpResponseRedirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model = Post
    fields = ['title', 'category', 'content']
    template_name = 'post_update_form.html'

    def get_login_url(self):
        return '/posts/{}'.format(self.kwargs['pk'])

    def test_func(self):
        return Post.objects.get(pk=self.kwargs['pk']).user.id == self.request.user.id


class UpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = UserProfile
    fields = ['url', 'description']
    template_name = 'profile_update_form.html'

    def get_success_url(self):
        return '/users/{}'.format(self.kwargs['pk'])

    def get_login_url(self):
        return '/users/{}'.format(self.kwargs['pk'])
    
    def test_func(self):
        return get_user_model().objects.get(pk=self.kwargs['pk']).userprofile.id == self.request.user.userprofile.id


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    template_name = "post_delete_form.html"

    def get_success_url(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if (post.category):
            return '/categories/{}/'.format(post.category.id)
        else:
            return '/'

    def test_func(self):
        return Post.objects.get(pk=self.kwargs['pk']).user.id == self.request.user.id


class UserView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = "user_posts"
    template_name = "profile.html"

    def get_queryset(self):
        queryset = Post.objects.filter(user_id=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requested_user = get_user_model().objects.get(id=self.kwargs['pk'])
        context['posts_count'] = Post.objects.filter(user=requested_user).count()
        context['requested_user'] = requested_user
        return context
