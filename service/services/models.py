from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_delete

from services.receivers import delete_cache_total_sum
from services.tasks import set_price, set_comment
from clients.models import Client


class Service(models.Model):
    name = models.CharField(max_length=100)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Now you can access the related subscriptions
        if self.__full_price != self.full_price:
            for subscription in self.subscriptions.all():
                set_comment.apply_async(args=[subscription.id], priority=5)
                set_price.apply_async(args=[subscription.id], priority=9)

        self.__full_price = self.full_price


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
        super().save(*args, **kwargs)

        if self.__discount_percentage != self.discount_percentage:
            for subscription in self.subscriptions.all():
                set_comment.apply_async(args=[subscription.id], priority=5)
                set_price.apply_async(args=[subscription.id], priority=9)

        # Update the internal value after the save operation
        self.__discount_percentage = self.discount_percentage

    def __str__(self):
        return self.plan_type


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.client} - {self.service} - {self.plan}'

    def save(self, *args, **kwargs):
        creating = not self.pk

        result = super().save(*args, **kwargs)
        if creating:
            set_price.apply_async(args=[self.id], priority=9)

        return result


post_delete.connect(delete_cache_total_sum, sender=Subscription)
