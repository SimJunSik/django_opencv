# Generated by Django 2.0.1 on 2018-09-11 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ex1_app', '0016_client_friendaddlist_friendlist_media_passid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnail',
            name='thumbnail_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]
