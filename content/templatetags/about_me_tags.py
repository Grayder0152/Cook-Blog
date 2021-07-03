from content.models import AboutPage
from django import template

register = template.Library()


@register.simple_tag()
def get_about_content():
    about_content = AboutPage.objects.prefetch_related('social_networks').first()
    return {'about_content': about_content}


@register.inclusion_tag('include/tags/about_me.html')
def get_about():
    about_page = AboutPage.objects.first()
    return {'about_page': about_page}


@register.inclusion_tag('include/tags/social_networks.html')
def get_social_networks():
    about_page = AboutPage.objects.prefetch_related('social_networks').first()
    social_networks = about_page.social_networks.all()
    return {'social_networks': social_networks}
