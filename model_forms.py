from django import forms
from django.utils.translation import ugettext_lazy as _


from . import models as blog_engine_models


class Tag(forms.ModelForm):

    class Meta:
        model = blog_engine_models.Tag
        fields = (
            'name',
        )
        widgets = {
            'name': forms.TextInput(),
        }


class Post(forms.ModelForm):

    class Meta:
        model = blog_engine_models.Post
        fields = (
            'title',
            'body',
            'body_markdown',
            'short_description',
            'tags',
            'visible',


        )
        widgets = {
            'title': forms.TextInput(),
            'body_markdown': forms.Textarea(attrs={
                'class': 'materialize-textarea wmd-input-markdown',
                'id': 'wmd-input-markdown'
            }),
            'body': forms.Textarea(attrs={
                'style': 'display: none;',

            }),
            'short_description': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'tags': forms.SelectMultiple(attrs={'class': 'browser-default select2'}),
        }

        labels = {
            'body': '',
        }


class Comment(forms.ModelForm):

    class Meta:
        model = blog_engine_models.Comment
        fields = (
            'comment',
        )

        widgets = {
            'comment': forms.TextInput()
        }


class ReplyToComment(forms.ModelForm):

    class Meta:
        model = blog_engine_models.ReplyToComment
        fields = (
            'reply_comment',
        )
        widget = {
            'reply_comment': forms.TextInput()
        }


class Author(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = blog_engine_models.AuthorProfile
        fields = (
            'first_name',
            'last_name',
            # 'image',
            'profile',
        )

        labels = {
            'first_name': _(u"First name"),
            'last_name': _(u"Last name"),
            # 'image': _(u"Profile Image"),
            'profile': _(u"Profile"),
        }
        widgets = {
            'profile': forms.Textarea(attrs={"class": "materialize-textarea"})
        }

    def save(self, commit=True):
        object = super(Author, self).save(commit=commit)
        if commit:
                user = object.user
                user.first_name = self.cleaned_data.get('first_name', "")
                user.last_name = self.cleaned_data.get('last_name', "")
                user.save()
        return object

