from django import forms

from . import model_forms as blog_engine_modelforms

Tag = forms.formset_factory(
    blog_engine_modelforms.Tag
)


