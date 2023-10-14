from django.http import JsonResponse

from movies.models import FilmWork


class MoviesApiMixin:
    http_method_names = ["get"]
    model = FilmWork

    def render_to_response(self, context: dict, **response_kwargs) -> JsonResponse:
        return JsonResponse(context)
