from django import forms
from .models import Comment, SubscribeEmail
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('create_at', 'post')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'website': forms.URLInput(attrs={'placeholder': 'Your website'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message'}),
        }


class EmailSubscribeForm(forms.ModelForm):
    email = forms.EmailField(label='',
                             widget=forms.EmailInput(attrs={'class': 'email-input', 'placeholder': 'Your email'}))

    class Meta:
        model = SubscribeEmail
        fields = ('email',)
