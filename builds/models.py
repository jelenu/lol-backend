from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Stat(models.Model):
    name = models.CharField(max_length=255)

class Item(models.Model):
    identification = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    colloq = models.CharField(max_length=255, blank=True)
    plaintext = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255)
    gold_base = models.IntegerField()
    gold_total = models.IntegerField()
    gold_sell = models.IntegerField()
    stats = models.ManyToManyField(Stat, through='ItemStat')
    item_from = models.ManyToManyField('self', symmetrical=False, related_name='crafts_into', blank=True)
    item_into = models.ManyToManyField('self', symmetrical=False, related_name='crafts_from', blank=True)
    tags = models.ManyToManyField(Tag)

class ItemStat(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    amount = models.IntegerField()


class RunePath(models.Model):
    id = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

class RuneSlot(models.Model):
    id = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    slot_number = models.IntegerField()
    rune_path = models.ForeignKey(RunePath, on_delete=models.CASCADE)
