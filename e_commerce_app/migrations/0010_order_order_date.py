# Generated by Django 4.2.5 on 2024-03-10 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce_app', '0009_alter_order_all_shoes'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(null=True),
        ),
    ]
