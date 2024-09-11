from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from services.tasks import set_price
from clients.models import Client


class Service(models.Model):
    name = models.CharField(max_length=100)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'FULL'),
        ('student', 'STUDENT'),
        ('discount', 'DISCOUNT')
    )

    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    discount_percentage = models.PositiveIntegerField(default=0,
                                                      validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.plan_type


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)

    def save(self, *args, save_model=True, **kwargs):
        if save_model:
            set_price.delay(self.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.client} - {self.service} - {self.plan}'
