# Generated by Django 4.2.4 on 2023-08-11 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("vote", "0001_initial"),
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="voted_polls",
            field=models.ManyToManyField(blank=True, to="vote.poll"),
        ),
    ]
