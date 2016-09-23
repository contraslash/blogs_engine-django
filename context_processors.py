from django.contrib.auth.context_processors import auth
from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject
from . import conf as blog_engine_conf

def blog_engine_urls(request):
    urls = {}
    urls['search_url'] = "%s:%s" % (blog_engine_conf.NAMESPACE, blog_engine_conf.POST_SEARCH_URL_NAME)
    return urls


def site_name(request):
    site = SimpleLazyObject(lambda: get_current_site(request))
    protocol = 'https' if request.is_secure() else 'http'
    print site
    return {
        'site': site,
        'site_root': SimpleLazyObject(lambda: "{0}://{1}".format(protocol, site.domain)),
        'full_url': SimpleLazyObject(lambda: "{0}://{1}{2}".format(protocol, site.domain, request.path)),
    }