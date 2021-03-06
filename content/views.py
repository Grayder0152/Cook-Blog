from .models import AboutPage
from django.shortcuts import render
from django.views.generic import View


class AboutView(View):
    def get(self, request):
        about_content = AboutPage.objects.all().prefetch_related('about_images')
        return render(request, 'content/about.html', {'about_content': about_content.first()})
