# Generated by Django 2.2 on 2021-03-19 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0010_auto_20210318_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='photo',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]