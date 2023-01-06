from django import forms

from .models import Comments


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=True)
    email = forms.EmailField(required=True)
    to = forms.EmailField(required=True)
    comments = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    """CommentForm definition."""

    class Meta:
        model = Comments
        fields = ('name', 'email', 'body')
