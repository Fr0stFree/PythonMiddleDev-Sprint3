import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True

    modified = models.DateTimeField(_("modified"), auto_now=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)


class UUIDMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
