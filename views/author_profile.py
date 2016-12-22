from django.contrib.auth import models as auth_models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django import http

from base import views as base_views

from .. import models as blog_engine_models
from .. import model_forms as blog_engine_forms
from .. import conf as blog_engine_conf


class Detail(base_views.BaseDetailView):
    model = blog_engine_models.AuthorProfile
    context_object_name = "author"

    def get_template_names(self):
        try:
            template_selected = blog_engine_models.Theme.objects.get(selected=True)
        except blog_engine_models.Theme.DoesNotExist:
            template_selected = blog_engine_models.Theme.objects.get(name="darkula")
        return ["blog_engine/themes/%s/author/detail.html" % template_selected.folder]

    def get_user(self):
        try:
            return auth_models.User.objects.get(username=self.kwargs.get("slug", ""))

        except auth_models.User.DoesNotExist:
            return None

    def get_object(self, queryset=None):
        user = self.get_user()
        if self.get_user() is not None:
            return blog_engine_models.AuthorProfile.objects.get(user=user)
        else:
            raise http.Http404

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)

        context['posts'] = blog_engine_models.Post.objects.filter(author=self.get_user()).order_by("-created")

        return context


class UpdateMe(base_views.BaseUpdateView):
    model = blog_engine_models.AuthorProfile
    form_class = blog_engine_forms.Author

    @method_decorator(login_required(login_url=reverse_lazy("log_in")))
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateMe, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return blog_engine_models.AuthorProfile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "%s:%s" % (blog_engine_conf.NAMESPACE, blog_engine_conf.AUTHOR_DETAIL_URL_NAME),
            kwargs={
                'slug': self.request.user.username
            }
        )