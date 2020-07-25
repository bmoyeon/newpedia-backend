from django.db import models

class Social(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'socials'

class Account(models.Model):
    nickname       = models.CharField(max_length = 50)
    social_account = models.CharField(max_length = 100)
    social         = models.ForeignKey('Social', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'accounts'
