from django.views.generic import TemplateView
from web.models import Category


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self):
        return {
            'categories': Category.objects.order_by('title')
        }


class ProfileView(TemplateView):
    template_name = "profile.html"


class AboutView(TemplateView):
    template_name = "about.html"
