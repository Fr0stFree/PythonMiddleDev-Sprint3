from typing import Any

from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.db.models import Q, F, QuerySet

from movies.models import FilmWork, Person
from .mixins import MoviesApiMixin


class MoviesListApiView(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_queryset(self) -> QuerySet[FilmWork]:
        return self.model.objects.prefetch_related("genres", "persons").all()


    def get_context_data(
        self, *, object_list=None, **kwargs
    ) -> dict[str, Any]:
        paginator, page, movies, is_paginated = self.paginate_queryset(
            self.get_queryset(), self.paginate_by
        )
        return


class MoviesDetailView(BaseDetailView, MoviesApiMixin):
    pass
