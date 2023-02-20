from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home-page"),
    path("all", views.all_page, name="all-page"),
    path("random", views.random_page, name="random-page"),
    path("filter/category/<str:category>", views.filter_category, name="filter-category"),
    path("filter/level/<str:level>", views.filter_level, name="filter-level"),
    path("filter/id/<int:id>", views.filter_id, name="filter-id"),
    path("add", views.add_page, name="add-page"),
    path("change", views.change_page, name="change-page"),
    path("update/<int:id>", views.update_page, name="update-page"),
    path("delete/<int:id>", views.delete_page, name="delete-page")
]
