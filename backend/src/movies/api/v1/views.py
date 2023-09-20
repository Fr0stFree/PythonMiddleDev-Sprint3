from typing import Any

from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from .mixins import MoviesApiMixin


class MoviesListApi(BaseListView, MoviesApiMixin):
    paginate_by = 10

    def get_context_data(
        self, *, object_list=None, **kwargs
    ) -> dict[str, Any]:
        paginator, page, movies, is_paginated = self.paginate_queryset(
            self.get_queryset(), self.paginate_by
        )
        return {"count": paginator.count, "results": movies}


class MoviesDetailView(BaseDetailView, MoviesApiMixin):
    pass
