from django.db import models

class Stat(models.Model):
    name = models.CharField(max_length=255)

class Item(models.Model):
    identification = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    colloq = models.CharField(max_length=255, blank=True)
    plaintext = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='item_images/')
    gold_base = models.IntegerField()
    gold_total = models.IntegerField()
    gold_sell = models.IntegerField()
    stats = models.ManyToManyField(Stat, through='ItemStat')
    item_from = models.ManyToManyField('self', symmetrical=False, related_name='crafts_into', blank=True)
    item_into = models.ManyToManyField('self', symmetrical=False, related_name='crafts_from', blank=True)

class ItemStat(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    amount = models.IntegerField()