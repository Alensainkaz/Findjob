"""Crawler-facing endpoints: root favicon, robots.txt, web manifest and the sitemap."""
from django.contrib.sitemaps import Sitemap
from django.contrib.staticfiles import finders
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.cache import cache_control

from .models import Resume

SITE = 'https://findy-job.com'


@cache_control(public=True, max_age=60 * 60 * 24 * 7)
def favicon(request):
    # Google looks for /favicon.ico at the site root, not under /static/
    path = finders.find('favicon.ico')
    if not path:
        raise Http404
    return FileResponse(open(path, 'rb'), content_type='image/x-icon')


@cache_control(public=True, max_age=60 * 60 * 24)
def robots_txt(request):
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /api/',
        'Disallow: /cart/',
        'Disallow: /create_resume/',
        'Disallow: /edit_resume/',
        'Disallow: /delete_resume/',
        '',
        f'Sitemap: {SITE}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines) + '\n', content_type='text/plain')


@cache_control(public=True, max_age=60 * 60 * 24)
def webmanifest(request):
    return JsonResponse({
        'name': 'Findy-Job',
        'short_name': 'Findy-Job',
        'description': 'Resume board for hiring in Kazakhstan',
        'start_url': '/',
        'display': 'standalone',
        'background_color': '#0b1622',
        'theme_color': '#0b1622',
        'icons': [
            {'src': static('favicon-192x192.png'), 'sizes': '192x192', 'type': 'image/png'},
            {'src': static('favicon-512x512.png'), 'sizes': '512x512', 'type': 'image/png'},
        ],
    }, content_type='application/manifest+json')


class CanonicalSitemap(Sitemap):
    """Always list URLs on the canonical host, whichever host served the sitemap."""
    protocol = 'https'

    def get_domain(self, site=None):
        return SITE.removeprefix('https://')


class StaticSitemap(CanonicalSitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)


class ResumeSitemap(CanonicalSitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Resume.objects.order_by('-created_at').only('pk', 'created_at')

    def location(self, obj):
        return reverse('resume_detail', args=[obj.pk])

    def lastmod(self, obj):
        return obj.created_at


sitemaps = {'static': StaticSitemap, 'resumes': ResumeSitemap}
