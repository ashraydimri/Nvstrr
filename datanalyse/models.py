from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class UserPorts(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    companies = models.CharField(max_length=15)
    quantity = models.IntegerField()
    boughtat = models.FloatField()

    def __str__(self):
        return (self.user).username

    def get_absolute_url(self):
        return reverse('datanalyse:detail',kwargs={'pk':self.pk})

class UserMoney(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    money=models.FloatField(default=2000000)

    def __str__(self):
        return (self.user).username

class TickerComp(models.Model):
    ticker = models.CharField(max_length=2000)
    name = models.CharField(max_length=2000)

    def __str__(self):
        return self.ticker

class BuyStockTable(models.Model):
    ticker = models.CharField(max_length=2000)
    name = models.CharField(max_length=2000)

    def __str__(self):
        return self.ticker
