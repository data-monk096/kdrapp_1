# Generated by Django 5.0 on 2024-01-20 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kdrapp_1', '0008_user_details_join_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='user_profile_pic/'),
        ),
    ]