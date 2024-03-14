# Generated by Django 4.2.5 on 2024-03-07 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce_app', '0003_alter_cart_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoeComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=100)),
                ('author_email', models.EmailField(max_length=254)),
                ('review', models.TextField()),
                ('review_star', models.IntegerField()),
                ('shoe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_commerce_app.shoe')),
            ],
        ),
    ]