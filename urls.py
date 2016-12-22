from django.conf.urls import url

from . import conf as blog_engine_conf

from .views import post as post_views
from .views import tag as tag_views
from .views import author_profile as author_views
urlpatterns = [
    url(
        r'^create/$',
        post_views.Create.as_view(),
        name=blog_engine_conf.POST_CREATE_URL_NAME
    ),
    url(
        r'^search/(?P<query>[\w|\W]+)/$',
        post_views.Search.as_view(),
        name=blog_engine_conf.POST_SEARCH_URL_NAME
    ),
    url(
        r'^tags/$',
        tag_views.List.as_view(),
        name=blog_engine_conf.TAG_LIST_URL_NAME
    ),
    url(
        r'^author/me/update$',
        author_views.UpdateMe.as_view(),
        name=blog_engine_conf.AUTHOR_UPDATE_ME_URL_NAME
    ),
    url(
        r'^author/(?P<slug>[\w-]+)/$',
        author_views.Detail.as_view(),
        name=blog_engine_conf.AUTHOR_DETAIL_URL_NAME
    ),
    url(
        r'^tag/(?P<slug>[\w-]+)/$',
        tag_views.Detail.as_view(),
        name=blog_engine_conf.TAG_DETAIL_URL_NAME
    ),
    url(
        r'^$',
        post_views.List.as_view(),
        name=blog_engine_conf.POST_LIST_URL_NAME
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        post_views.Detail.as_view(),
        name=blog_engine_conf.POST_DETAIL_URL_NAME
    ),
    url(
        r'^(?P<slug>[\w-]+)/update/$',
        post_views.Update.as_view(),
        name=blog_engine_conf.POST_CREATE_URL_NAME
    ),


]
