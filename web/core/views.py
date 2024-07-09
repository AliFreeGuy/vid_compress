from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, permissions
from rest_framework.serializers import ValidationError
from . import serializers
from accounts.models import User
from django.http import JsonResponse
from . import models




class RemoveSubUserAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self , request ):
        chat_id = request.data.get('chat_id')
        user = User.objects.filter(chat_id = int(chat_id))
        if user.exists() :
            user = user.first()
            user_plans  = models.UserPlanModel.objects.filter(user = user)
            print(user_plans)
            if user_plans :
                user_plans.first().delete()
                return JsonResponse({'status' : 'ok'})
        return JsonResponse({'status' : 'no'})


        






class AddSubUserAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self , request):
        chat_id = request.data.get('chat_id')
        plan_tag = request.data.get('plan_tag')
        user = User.objects.filter(chat_id = int(chat_id))
        plan = models.PlansModel.objects.filter(tag = plan_tag)
        if user.exists() and plan.exists():
            user = user.first()
            bot = models.BotModel.objects.first()
            plan = plan.first()
            models.UserPlanModel.objects.create(user = user , plan = plan , bot = bot)
            return JsonResponse({'status' : 'ok'})
        return JsonResponse({'status' : 'no'})




class UserUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try :
            chat_id = request.data.get('chat_id')
            if not chat_id:
                return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(chat_id=chat_id).first()
            
            if user:
                serializer = serializers.UserSerializer(user, data=request.data, partial=True)
            else:
                serializer = serializers.UserSerializer(data=request.data)
            
            if serializer.is_valid():
                user = serializer.save()
                return Response(serializers.UserSerializer(user).data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return JsonResponse({'error' : str(e)})




class SettingAPIView(APIView):
    authentication_classes = [TokenAuthentication ,]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        setting = models.SettingModel.objects.first()
        serializer = serializers.SettingSerializer(setting)
        return Response(serializer.data , status=status.HTTP_200_OK)
    




class PlansAPIView(APIView):
    authentication_classes = [TokenAuthentication ,]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def get(self , request ):
        plans = models.PlansModel.objects.filter(is_active = True)
        ser_data = serializers.PlanSerializer(plans , many = True)
        return Response(ser_data.data)
    


