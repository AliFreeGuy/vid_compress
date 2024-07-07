from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
import datetime

class BotModel(models.Model):
    name = models.CharField(max_length = 128 , unique = True)
    username = models.CharField(max_length = 128 , unique = True)
    token = models.CharField(max_length= 128 , unique = True)
    api_hash = models.CharField(max_length = 225)
    api_id = models.CharField(max_length = 225)

    def __str__(self) -> str:
        return str(self.name)

    class Meta :
        verbose_name = "My Bots"
        verbose_name_plural = "My Bots"



class PlansModel(models.Model):
    bot = models.ForeignKey(BotModel , on_delete = models.CASCADE , related_name = 'plans')
    tag = models.CharField(max_length = 128  , unique = True)
    name_fa = models.CharField(max_length = 128, unique = True) 
    name_en = models.CharField(max_length = 128, unique = True)
    des_fa= models.TextField()
    des_en= models.TextField()
    day = models.IntegerField()
    volume = models.IntegerField()
    is_active = models.BooleanField(default = True)


    def __str__(self) -> str:
        return str(self.name_fa)
    

    class Meta :
        verbose_name = "Plans"
        verbose_name_plural = "Plans"



class SettingModel(models.Model):


    bot = models.ForeignKey(BotModel , on_delete = models.CASCADE , verbose_name = 'telegram bot')
    video_limit = models.IntegerField(default = 500)
    admin_chat_id = models.IntegerField(verbose_name = 'chat_id admin')
    watermark_text = models.CharField(max_length = 32 ,null = True , blank = True)
    channel_url  = models.CharField(max_length = 128 , null = True , blank = True)
    channel_chat_id  = models.IntegerField( null = True , blank = True)
    channel_text_fa = models.TextField(default = 'خالی')
    channel_text_en = models.TextField(default = 'خالی')

    start_text_fa = models.TextField()
    start_text_en = models.TextField()

    plans_text_fa = models.TextField()
    plans_text_en = models.TextField()

    help_text_fa = models.TextField()
    help_text_en = models.TextField()

    sup_text_fa = models.TextField()
    sup_text_en = models.TextField()

    join_text_fa = models.TextField()
    join_text_en = models.TextField()


    setting_text_fa = models.TextField()
    setting_text_en = models.TextField()


    placeholder_text_fa = models.CharField(max_length=128)
    placeholder_text_en = models.CharField(max_length=128)


    quality_1 = models.IntegerField(
        validators=[
            MinValueValidator(100),
            MaxValueValidator(500)
        ]
     , default = 100)
    quality_2 = models.IntegerField(
        validators=[
            MinValueValidator(100),
            MaxValueValidator(500)
        ]
    , default = 100)
    quality_3 = models.IntegerField(
        validators=[
            MinValueValidator(100),
            MaxValueValidator(500)
        ]
    , default = 100)

    def __str__(self) -> str:
        return 'Setting'
    
    
    class Meta :
        verbose_name = "Setting"
        verbose_name_plural = "Setting"




class UserPlanModel(models.Model ):

    bot = models.ForeignKey(BotModel , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='plans')
    plan = models.ForeignKey(PlansModel , on_delete=models.CASCADE , related_name='users')
    expiry = models.DateTimeField(null=True , blank = True )
    volume = models.BigIntegerField(default=0 , null=True , blank=True)
    is_active = models.BooleanField(default=True)



    def __str__(self) -> str:
        return str(self.user)
    
    class Meta :
        verbose_name = "Subscription"
        verbose_name_plural = "Subscription"
    
    def save(self, *args, **kwargs):
        active_subscription = UserPlanModel.objects.filter(user=self.user, is_active=True).exclude(id=self.id).first()
        if active_subscription:
            active_subscription.delete()
        
        data = UserPlanModel.objects.filter(id=self.id)

        if self.plan and not data.exists():
            self.expiry = datetime.datetime.now() + datetime.timedelta(days=int(self.plan.day))
            self.volume = self.plan.volume
        




        super().save(*args, **kwargs)
