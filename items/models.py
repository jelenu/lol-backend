from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Stat(models.Model):
    name = models.CharField(max_length=255)

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    colloq = models.CharField(max_length=255, blank=True,)
    plaintext = models.CharField(max_length=255, blank=True,)
    item_from = ArrayField(models.CharField(max_length=500), blank=True, default=list)
    image = models.CharField(max_length=15)
    gold_base = models.IntegerField()
    gold_total = models.IntegerField()
    gold_sell = models.IntegerField()
    stats = models.ManyToManyField(Stat, through='ItemStat')
    item_from = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    item_into = ArrayField(models.CharField(max_length=255), blank=True, default=list)

class ItemStat(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    amount = models.IntegerField()



