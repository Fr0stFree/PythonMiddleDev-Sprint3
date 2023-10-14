from typing import Any

from django.db.models import QuerySet
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork
from .mixins import MoviesApiMixin
from .serializers import serialize_film_work


class MoviesDetailApiView(MoviesApiMixin, BaseDetailView):
    pk_url_kwarg = "id"

    def get_object(self, queryset=None) -> FilmWork:
        return self.model.objects.prefetch_related("genres", "persons").get(id=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        film_work = self.get_object()
        return serialize_film_work(film_work)


class MoviesListApiView(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_queryset(self) -> QuerySet[FilmWork]:
        return self.model.objects.prefetch_related("genres", "persons").all()

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, Any]:
        paginator, page, film_works, is_paginated = self.paginate_queryset(self.get_queryset(), self.paginate_by)
        results = [serialize_film_work(film_work) for film_work in film_works]
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": results,
        }
