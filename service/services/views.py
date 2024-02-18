
from django.db.models import Prefetch, Sum, F
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subscription
from .serializers import SubscriptionSerializer
from clients.models import Client


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related('plan',
                                                           'service',
        Prefetch('client', queryset=Client.objects.all().select_related('user')
                 .only('company_name', 'user__email'))).annotate(price=F('service__full_price')
                                                                       - F('service__full_price')*(F('plan__discount')/100.00))
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {'results': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data

        return response

