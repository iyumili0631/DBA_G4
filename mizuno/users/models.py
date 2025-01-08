from django.db import models

# Create your models here.

# 使用者賬號密碼
class User(models.Model):
    user_ID = models.IntegerField()
    user_name = models.CharField(max_length=255)
    user_account = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)