from django.conf.urls import patterns, include, url
from friendly.topcoat import urls as topcoat_urls
from django.views.generic import TemplateView

urlpatterns = patterns('',
    (r'^$', TemplateView.as_view(template_name="example.html")),
)
