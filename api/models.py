from django.db import models


class Categories(models.Model):
    name = models.CharField('Наименование', unique=True, max_length=255)
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name="Родитель", related_name='child',
                               on_delete=models.CASCADE)
