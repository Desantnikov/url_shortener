from django.contrib import admin
from django.urls import path, re_path

from url_shortener.views import UrlListView, UrlView, RedirectView

app_name = 'url_shortener'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/url/', UrlListView.as_view()),
    re_path('api/url/(?P<short_id>[A-z0-9]{1,6})/', UrlView.as_view()),
    re_path(r'^(?P<short_id>[A-z0-9]{1,6})/', RedirectView.as_view())
]
