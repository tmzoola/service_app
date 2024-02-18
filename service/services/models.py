from django.db import models
from django.core.validators import MaxValueValidator

from clients.models import Client


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - ${self.full_price}"

class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student','Student'),
        ('discount','Discount')
    )

    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    discount = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(100)])

    def __str__(self):
        return f"{self.plan_type} - {self.discount}%"



class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service,related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan,related_name='subscriptions', on_delete=models.PROTECT)
