# Generated by Django 2.0.1 on 2018-09-04 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ex1_app', '0014_thumbnail_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='thumbnail',
            name='user_id',
            field=models.CharField(default='none', max_length=20),
        ),
    ]
