# Generated by Django 2.2 on 2021-03-18 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fan', '0001_initial'),
        ('artist', '0005_auto_20210317_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='followed_by',
            field=models.ManyToManyField(null=True, related_name='artist_followed_by', to='fan.Fan'),
        ),
    ]
