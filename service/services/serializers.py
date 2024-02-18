from rest_framework import serializers

from .models import Subscription, Plan



class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    client_name = serializers.CharField(source='client.company_name')
    email = serializers.EmailField(source='client.user.email')
    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        return  (instance.service.full_price -
                 instance.service.full_price *(instance.plan.discount/100))

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'email','plan','price')
