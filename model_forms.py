from django import forms

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
