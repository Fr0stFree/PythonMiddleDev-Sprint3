from typing import Any

from movies.models import FilmWork, PersonFilmWork


def serialize_film_work(film_work: FilmWork) -> dict[str, Any]:
    jenres = film_work.genres.values_list("name", flat=True)
    persons = film_work.persons.all()
    actors = persons.filter(
        personfilmwork__role=PersonFilmWork.Roles.ACTOR
    ).values_list("full_name", flat=True)
    directors = persons.filter(
        personfilmwork__role=PersonFilmWork.Roles.DIRECTOR
    ).values_list("full_name", flat=True)
    writers = persons.filter(
        personfilmwork__role=PersonFilmWork.Roles.PRODUCER
    ).values_list("full_name", flat=True)
    return {
        "id": film_work.id,
        "title": film_work.title,
        "description": film_work.description,
        "creation_date": film_work.creation_date,
        "rating": film_work.rating,
        "type": film_work.type,
        "jenres": list(jenres),
        "actors": list(actors),
        "directors": list(directors),
        "writers": list(writers),
    }
