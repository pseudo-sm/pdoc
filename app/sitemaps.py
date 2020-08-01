from django.contrib.sitemaps import Sitemap
from .models import Type


class CategorySitemap(Sitemap):
    changefreq = "always"
    priority = 0.9

    def items(self):
        return Type.objects.all()

