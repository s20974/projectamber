from django.db import models
from authapp.models import User


class Task(models.Model):
    # task title
    title = models.CharField(max_length=50, help_text="Enter task title")
    # task description
    description = models.CharField(max_length=500, help_text="Enter task description")
    # task icon
    bootstrap_icon = models.CharField(max_length=500, help_text="Enter bootstrap icon here")
    # form link
    link = models.CharField(max_length = 100, help_text="Путь к настройке задания")

    def __str__(self):
        return self.title

# Useful links on account/actions
class Action(models.Model):
    # title
    title = models.CharField(max_length=50, help_text="Provide name of your service")
    # description
    description = models.CharField(max_length=500, help_text="Provide short decription")
    # action icon
    bootstrap_icon = models.CharField(max_length=500, help_text="Enter bootstrap icon here")
    # action link
    link = models.CharField(max_length=100,help_text='Provide link to an action')

    def __str__(self):
        return self.title

# just tokens' models
class ViberToken(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " - " + str(self.owner)


class TelegramToken(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " - " + str(self.owner)

# model for groups of tokens
class Group(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    telegram_tokens = models.ManyToManyField(TelegramToken)
    viber_tokens = models.ManyToManyField(ViberToken)

    def __str__(self):
        return self.name + " - " + str(self.owner)
