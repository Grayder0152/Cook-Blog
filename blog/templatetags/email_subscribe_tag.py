from blog.forms import EmailSubscribeForm
import random
from django import template

register = template.Library()


@register.simple_tag()
def get_email_subscribe_form():
    email_subscribe = EmailSubscribeForm()
    return {'email_subscribe': email_subscribe, 'random_id': random.random()}
