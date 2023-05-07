from django.urls import path

from .views import homePage, detailPage, createPage, updatePage, deletePage

app_name = "todo_app"

urlpatterns = [
    path('', homePage, name="home-page"),
    path('create/', createPage, name="create-page"),
    path('task/<int:pk>/', detailPage, name="detail-page"),
    path('update/<int:pk>/', updatePage, name="update-page"),
    path('delete/<int:pk>/', deletePage, name="delete-page"),
]