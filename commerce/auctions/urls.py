from django.urls import path, re_path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = "commerce"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories/", views.categories, name="categories"),
    re_path("category/(?:(?P<category>.+)/)?$",
            views.category, name="category"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("winner/", views.winner, name="winner"),
    path("auction/<str:title>", views.auction, name="auction"),
    path("bid/<str:title>", views.bid, name="bid"),
    path("comment/<str:title>", views.comment, name="comment"),
    path("watch/<int:id>",
         views.watch, name="watch"),
    path("delete/<int:id>", views.delete, name="delete"),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
