from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subscription
from .serializers import SubscriptionSerializer
from clients.models import Client


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related('plan',
                                                           'service',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')))
    serializer_class = SubscriptionSerializer
