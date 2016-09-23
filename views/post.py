
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.utils.text import slugify
from django.db import IntegrityError
from django.template.loader import get_template
from django.utils.encoding import iri_to_uri, uri_to_iri
from django.utils.http import urlquote

from utils import utils

from base import views as base_views

from .. import model_forms as blog_engine_modelforms
from .. import models as blog_engine_models
from .. import formsets as blog_engine_formsets
from .. import conf as blog_engine_conf


class Create(base_views.BaseCreateView):
    form_class = blog_engine_modelforms.Post

    def get_template_names(self):
        try:
            template_selected = blog_engine_models.Theme.objects.get(selected=True)
        except blog_engine_models.Theme.DoesNotExist:
            template_selected = blog_engine_models.Theme.objects.get(name="darkula")
        return ["blog_engine/themes/%s/post/create.html" % template_selected.folder]

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('blog_engine.add_post'):
            return super(Create, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotFound(get_template("403.html").render())

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = blog_engine_formsets.Tag(self.request.POST)
        else:
            context['formset'] = blog_engine_formsets.Tag()

        return context

    def form_valid(self, form):
        print "Form Valid"
        context = self.get_context_data(form=form)
        valid_tags = []
        post = form.save(commit=False)
        post.author = self.request.user
        try:
            post.slug = slugify(post.title)
            post.save()
        except IntegrityError:
            post.slug = slugify(post.title + " " + utils.generate_random_string(4))
            post.save()

        post.save()
        form.save_m2m()
        print post.tags
        for innerform in context['formset']:
            if innerform.is_valid():
                print "Inner form Valid"
                print innerform
                valid_innerform = innerform.save(commit=False)
                if valid_innerform.name:
                    try:
                        valid_innerform.slug = slugify(valid_innerform.name)
                        valid_innerform.save()
                    except IntegrityError:
                        valid_innerform.slug = slugify(valid_innerform.name + " " + utils.generate_random_string(4))
                        valid_innerform.save()
                    valid_tags.append(valid_innerform)
                    post.tags.add(valid_innerform)
                else:
                    print "Empty Tags"
            else:
                print 'Inner form invalid'
                print innerform

        print valid_tags
        print post.tags
        post.save()
        return HttpResponseRedirect(
            reverse_lazy(
                "%s:%s" % (blog_engine_conf.NAMESPACE, blog_engine_conf.POST_DETAIL_URL_NAME),
                kwargs={
                    'slug': post.slug
                }
            ))

    def form_invalid(self, form):
        print "Form INVALID"

        context = self.get_context_data(form=form)

        return self.render_to_response(context)


class List(base_views.BasePaginationListView):
    queryset = blog_engine_models.Post.objects.filter(visible=True).order_by("-id")
    elements_by_page = blog_engine_conf.POST_BY_PAGE

    def get_template_names(self):
        try:
            template_selected = blog_engine_models.Theme.objects.get(selected=True)
        except blog_engine_models.Theme.DoesNotExist:
            template_selected = blog_engine_models.Theme.objects.get(name="darkula")
        print template_selected
        return ["blog_engine/themes/%s/post/list.html" % template_selected.folder]


class Detail(base_views.BaseDetailView):

    model = blog_engine_models.Post
    context_object_name = "post"

    def get_template_names(self):
        try:
            template_selected = blog_engine_models.Theme.objects.get(selected=True)
        except blog_engine_models.Theme.DoesNotExist:
            template_selected = blog_engine_models.Theme.objects.get(name="darkula")
        return ["blog_engine/themes/%s/post/detail.html" % template_selected.folder]


class Update(generic.UpdateView):
    model = blog_engine_models.Post
    form_class = blog_engine_modelforms.Post

    def get_template_names(self):
        try:
            template_selected = blog_engine_models.Theme.objects.get(selected=True)
        except blog_engine_models.Theme.DoesNotExist:
            template_selected = blog_engine_models.Theme.objects.get(name="darkula")
        return ["blog_engine/themes/%s/post/create.html" % template_selected.folder]

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('blog_engine.change_post'):
            return super(Update, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotFound(get_template("403.html").render())

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = blog_engine_formsets.Tag(self.request.POST)
        else:
            context['formset'] = blog_engine_formsets.Tag()

        return context

    def form_valid(self, form):
        print "Form Valid"
        context = self.get_context_data(form=form)
        valid_tags = []
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        form.save_m2m()
        print post.tags
        for innerform in context['formset']:
            if innerform.is_valid():
                print "Inner form Valid"
                print innerform
                valid_innerform = innerform.save(commit=False)
                if valid_innerform.name:
                    try:
                        valid_innerform.slug = slugify(valid_innerform.name)
                        valid_innerform.save()
                    except IntegrityError:
                        valid_innerform.slug = slugify(valid_innerform.name + " " + utils.generate_random_string(4))
                        valid_innerform.save()
                    valid_tags.append(valid_innerform)
                    post.tags.add(valid_innerform)
                else:
                    print "Empty Tags"
            else:
                print 'Inner form invalid'
                print innerform

        print valid_tags
        print post.tags
        post.save()
        return HttpResponseRedirect(
            reverse_lazy(
                "%s:%s" % (blog_engine_conf.NAMESPACE, blog_engine_conf.POST_DETAIL_URL_NAME),
                kwargs={
                    'slug': post.slug
                }
            ))

class Search(base_views.BasePaginationListView):
    elements_by_page = blog_engine_conf.POST_BY_PAGE

    def get_template_names(self):
        try:
            template_selected = blog_engine_models.Theme.objects.get(selected=True)
        except blog_engine_models.Theme.DoesNotExist:
            template_selected = blog_engine_models.Theme.objects.get(name="darkula")
        print template_selected
        return ["blog_engine/themes/%s/post/list.html" % template_selected.folder]

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)

        context['query'] = uri_to_iri(self.kwargs.get('query'))
        busqueda = context['query']

        print uri_to_iri(busqueda)
        return context

    def get_queryset(self):
        query = uri_to_iri(self.kwargs.get('query',"").strip())
        return blog_engine_models.Post.objects.filter(body_markdown__icontains=query)

    def post(self, request, *args, **kwargs):
        busqueda = None

        try:
            busqueda = request.POST.get('query', None)

        except KeyError:
            pass
        if busqueda is not None:
            # print busqueda.decode('ascii')
            # print iri_to_uri(urlquote(busqueda))
            return HttpResponseRedirect(reverse_lazy(
                "%s:%s" % (blog_engine_conf.NAMESPACE, blog_engine_conf.POST_SEARCH_URL_NAME),
                kwargs={
                    "query": iri_to_uri(urlquote(busqueda))
                }))
        return HttpResponseRedirect(reverse_lazy(
            "%s:%s" % (blog_engine_conf.NAMESPACE, blog_engine_conf.POST_LIST_URL_NAME)
        ))