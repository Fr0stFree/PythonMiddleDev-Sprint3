from django.urls import path

from movies.api.v1 import views

urlpatterns = [
    path("movies/", views.MoviesListApiView.as_view(), name="movies-list"),
]
