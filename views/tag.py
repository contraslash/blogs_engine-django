from django.views import generic
from .. import model_forms as blog_engine_model_forms
from .. import models as blog_engine_models


class Detail(generic.DetailView):
    template_name = "blog_engine/tag/detail.html"
    model = blog_engine_models.Tag

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)

        print context['object']

        all_posts = blog_engine_models.Post.objects.all()
        for post in all_posts:
            print unicode(post) + unicode(post.tags.all())

        context['posts'] = blog_engine_models.Post.objects.filter(tags=context['object'])
        print context['posts']

        return context


