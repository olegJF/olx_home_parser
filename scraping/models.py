import jsonfield
from django.db import models


class RealEstate(models.Model):
    url = models.URLField(unique=True, db_index=True)
    title = models.CharField(max_length=250)
    # description = models.TextField(blank=True)
    price = models.CharField(max_length=50)
    added_time = models.PositiveSmallIntegerField(blank=True, null=True)
    sent = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    history_data = jsonfield.JSONField()
    last_price = models.PositiveIntegerField(verbose_name='Last price',
                                             default=0)

    def __str__(self):
        return self.title
