from .models import Comment
from django import forms


class EmailPostForm(forms.ModelForm):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.post = self.cleaned_data['post']
    #     if commit:
    #         instance.save()
    #     return instance