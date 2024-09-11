from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from services.tasks import set_price
from clients.models import Client


class Service(models.Model):
    name = models.CharField(max_length=100)
    full_price = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):

        if self.__full_price != self.full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percentage = self.discount_percentage

    def save(self, *args, **kwargs):

        if self.__discount_percentage != self.discount_percentage:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.plan_type


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.client} - {self.service} - {self.plan}'
