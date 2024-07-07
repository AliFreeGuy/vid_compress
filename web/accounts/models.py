from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser , PermissionsMixin):
    QUALITY_CHOICES = [
        ('q1', 'Quality 1'),
        ('q2', 'Quality 2'),
        ('q3', 'Quality 3'),
    ]

    LANG_CHOICES = [
        ('fa', 'Farsi'),
        ('en', 'English'),
    ]


    chat_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=128 , null=True ,blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    creation = models.DateTimeField(auto_now_add=True)
    lang = models.CharField(max_length=2, choices=LANG_CHOICES, default='fa')
    quality = models.CharField(max_length=2, choices=QUALITY_CHOICES, null=True, blank=True)

    USERNAME_FIELD = 'chat_id'
    REQUIRED_FIELDS = ['full_name' , ]

    objects = UserManager()


    def __str__(self) -> str:
        return f'{str(self.chat_id)} - {self.full_name}'
    

    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta :

        verbose_name = "All Users"
        verbose_name_plural = "All Users"