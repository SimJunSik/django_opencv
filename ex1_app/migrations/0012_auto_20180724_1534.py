# Generated by Django 2.0.1 on 2018-07-24 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ex1_app', '0011_auto_20180716_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnail',
            name='thumbnail_id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
    ]
