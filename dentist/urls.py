from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    def items(self):
        return ['home', 'about', 'service', 'pricing', 'contact', 'blog1', 'blog2', 'blog3']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'static': StaticSitemap(),
}



urlpatterns = [
    path('admin/', admin.site.urls),

    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    )),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    path("", include("website.urls")),
]