# Generated by Django 2.2.12 on 2020-04-29 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nano_poker', '0003_auto_20200429_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_name',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='policy_name',
            field=models.CharField(max_length=64, null=True),
        ),
    ]