from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from . import views

urlpatterns = [
    path("icon_img.ico", views.favicon),
    path("", views.home_page, name="home"),
    path("proteins/", views.get_database, name="proteins"),
    re_path(
        r"^proteins/(?P<gene>[-\w]+)/$", # gene is SlugField with name of gene
        # {'my_id': '?P<my_id>'}
        views.ProteinDetailView.as_view(),
        name="protein-detail",
    ),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

