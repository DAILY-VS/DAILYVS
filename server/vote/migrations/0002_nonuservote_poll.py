# Generated by Django 4.2.3 on 2023-08-06 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonuservote',
            name='poll',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='vote.poll'),
            preserve_default=False,
        ),
    ]
