from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("list", views.ArticleViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("rate/", views.RateView.as_view(), name="rate"),
    path("categories/", views.CategoryView.as_view(), name="categories"),
    path("rating/", views.ArticleRatingsView.as_view(), name="rating")
]
