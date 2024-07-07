from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('api/user_update/' , views.UserUpdateAPIView.as_view() , name='user_update'),
    path('api/setting/', views.SettingAPIView.as_view() , name='setting'),
    path('api/plans/' , views.PlansAPIView.as_view() ,name='plans') ,

]