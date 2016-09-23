
from django.http import HttpResponseNotFound

from django.template.loader import get_template

from base import views

from .. import model_forms as blog_engine_model_forms
from .. import models as blog_engine_models


class Detail(views.BasePaginationListView):
    model = blog_engine_models.Tag
    tag = None
    elements_by_page = 5
    ordering = "created"

    def get_template_names(self):
        try:
            template_selected = blog_engine_models.Theme.objects.get(selected=True)
        except blog_engine_models.Theme.DoesNotExist:
            template_selected = blog_engine_models.Theme.objects.get(name="darkula")
        return ["blog_engine/themes/%s/tag/detail.html" % template_selected.folder]

    def dispatch(self, request, *args, **kwargs):
        try:
            self.tag = blog_engine_models.Tag.objects.get(slug=self.kwargs['slug'])
            return super(Detail, self).dispatch(request, *args, **kwargs)
        except blog_engine_models.Tag.DoesNotExist:
            return HttpResponseNotFound(get_template("403.html").render())

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)

        context['tag'] = self.tag

        return context

    def get_queryset(self):
        return blog_engine_models.Post.objects.filter(tags=self.tag).order_by("-id")

    #
    # def get_context_data(self, **kwargs):
    #     context = super(Detail, self).get_context_data(**kwargs)
    #
    #     context['object'] = self.tag
    #
    #     print context['object']
    #     context['posts'] = blog_engine_models.Post.objects.filter(tags=context['object'])
    #
    #     return context


