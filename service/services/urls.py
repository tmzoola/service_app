from django.urls import path

from . import views

urlpatterns = [
    path('api/subscriptions/', views.SubscriptionView.as_view({'get': 'list'}))
]