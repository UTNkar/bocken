from django.db import models
from django.core.cache import cache


class SingletonModel(models.Model):
    """
    A singleton model only has one row in its table in the database.

    This prevent that multiple rows are created, containing different
    informtaion which can cause problems and confusion.

    This class uses a cache to decrease the amount of fetches to the database.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):  # noqa
        """Save the changes to first row in the database."""
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

        self.set_cache()

    def delete(self, *args, **kwargs):
        """Rows should not be deletable."""
        pass

    @classmethod
    def load(cls):
        """Get the current settings."""
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

    def set_cache(self):  # noqa
        cache.set(self.__class__.__name__, self)
