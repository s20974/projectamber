# Generated by Django 3.0.7 on 2020-07-08 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200708_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='jointproduct',
            name='partners',
            field=models.IntegerField(default=2, verbose_name='Макс. участников'),
        ),
    ]
