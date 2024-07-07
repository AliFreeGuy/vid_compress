from rest_framework import serializers
from .models import SettingModel , UserPlanModel , PlansModel
from accounts.models import User



class PlanSerializer(serializers.ModelSerializer):
    class Meta :
        model = PlansModel
        fields = '__all__'


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingModel
        fields = '__all__'



class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlanModel
        fields = '__all__'




class UserSerializer(serializers.ModelSerializer):
    sub = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_sub(self, obj):
        user_subs = obj.plans.filter(is_active = True).first()
        serializer = UserPlanSerializer(user_subs)
        return serializer.data
