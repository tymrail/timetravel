from django import forms


class BlogForm(forms.Form):
    title = forms.CharField(label='标题')
    author = forms.CharField(label='作者')
    content = forms.CharField(label='正文', widget=forms.Textarea)