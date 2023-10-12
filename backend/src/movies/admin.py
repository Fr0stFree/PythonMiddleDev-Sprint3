from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 2
    verbose_name = _("genre")
    verbose_name_plural = _("genres")


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 2
    verbose_name = _("person_film_work")
    verbose_name_plural = _("person_film_works")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "total_movies")
    search_fields = ("name",)
    list_filter = ("modified",)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY

    def total_movies(self, obj: Genre) -> int:
        return obj.film_works.count()

    total_movies.short_description = _("total_movies_exist_in_genre")


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "description", "creation_date", "rating")
    search_fields = ("title", "type")
    list_filter = ("creation_date", "rating")
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "total_movies")
    list_filter = ("full_name",)
    search_fields = ("full_name",)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY

    def total_movies(self, obj: Person) -> int:
        return FilmWork.objects.filter(persons=obj).count()

    total_movies.short_description = _("total_movies_played_by_actor")
