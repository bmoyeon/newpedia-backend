from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'menus'

class Category(models.Model):
    name = models.CharField(max_length = 50)
    menu = models.ForeignKey('Menu', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'categories'

class Word(models.Model):
    name        = models.CharField(max_length = 200)
    description = models.CharField(max_length = 2000)
    example     = models.CharField(max_length = 1000, blank = True)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)
    account     = models.ManyToManyField('account.Account', through = 'WordAccount')
    category    = models.ManyToManyField('Category', through = 'WordCategory')

    class Meta:
        db_table = 'words'

class WordCategory(models.Model):
    word     = models.ForeignKey('Word', on_delete = models.CASCADE)
    category = models.ForeignKey('Category', on_delete = models.CASCADE)

    class Meta:
        db_table = 'word_categories'

class WordAccount(models.Model):
    word       = models.ForeignKey('Word', on_delete = models.CASCADE)
    account    = models.ForeignKey('account.Account', on_delete = models.CASCADE)
    like       = models.BooleanField(default = False)
    dislike    = models.BooleanField(default = False)
    is_created = models.BooleanField(default = 0)
    is_updated = models.BooleanField(default = 0)

    class Meta:
        db_table = 'word_accounts'
