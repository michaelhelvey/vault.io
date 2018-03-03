from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class ProfileView(TemplateView):
    template_name = "profile.html"


class AboutView(TemplateView):
    template_name = "about.html"
