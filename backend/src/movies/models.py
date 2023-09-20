from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin


class Genre(UUIDMixin, TimeStampedMixin):
    class Meta:
        db_table = '"content"."genre"'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(
        blank=True,
        default="",
        verbose_name=_("description"),
    )

    def __str__(self):
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):
    class Meta:
        db_table = '"content"."film_work"'
        verbose_name = _("film_work")
        verbose_name_plural = _("film_works")

    title = models.CharField(_("title"), max_length=255)
    type = models.CharField(_("type"), max_length=255)
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
        default="",
    )
    creation_date = models.DateField(
        verbose_name=_("creation_date"),
        null=True,
        db_index=True,
    )
    rating = models.FloatField(
        verbose_name=_("rating"),
        null=True,
        blank=True,
        db_index=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    genres = models.ManyToManyField(
        to=Genre,
        through="GenreFilmWork",
        related_name="film_works",
        verbose_name=_("genres"),
    )
    persons = models.ManyToManyField(
        to="Person",
        through="PersonFilmWork",
        related_name="film_works",
        verbose_name=_("persons"),
    )

    def __str__(self):
        return f"{self.title}"


class GenreFilmWork(UUIDMixin):
    class Meta:
        db_table = '"content"."genre_film_work"'
        unique_together = ("film_work_id", "genre_id")
        verbose_name = _("genre_film_work")
        verbose_name_plural = _("genre_film_works")

    created = models.DateTimeField(_("created"), auto_now_add=True)
    film_work = models.ForeignKey(
        to=FilmWork,
        verbose_name=_("film_work"),
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        to=Genre,
        verbose_name=_("genre"),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.film_work} - {self.genre}"


class Person(UUIDMixin, TimeStampedMixin):
    class Meta:
        db_table = '"content"."person"'
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    full_name = models.CharField(_("full_name"), max_length=255)

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    class Meta:
        db_table = '"content"."person_film_work"'
        unique_together = ("film_work_id", "person_id", "role")
        verbose_name = _("person_film_work")
        verbose_name_plural = _("persons_film_works")

    class Roles(models.TextChoices):
        ACTOR = "actor", _("actor")
        PRODUCER = "writer", _("writer")
        DIRECTOR = "director", _("director")

    created = models.DateTimeField(_("created"), auto_now_add=True)
    role = models.CharField(
        verbose_name=_("role"),
        choices=Roles.choices,
        max_length=64,
    )
    person = models.ForeignKey(
        to=Person,
        verbose_name=_("person"),
        on_delete=models.CASCADE,
    )
    film_work = models.ForeignKey(
        to=FilmWork,
        verbose_name=_("film_work"),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.person} - {self.role} - {self.film_work}"
