from django import forms
from .models import Post_in_site


class PostForm(forms.ModelForm):
    class Meta:
        model = Post_in_site
        fields = ['text_for_post']
        widgets = {
            'text_for_post': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'text_for_post': 'Ваш пост',
        }
