# Generated by Django 4.1.3 on 2022-11-10 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rss", "0002_remove_userrssitemmodel_user_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="rssitemmodel",
            old_name="users",
            new_name="user_rss",
        ),
        migrations.RenameField(
            model_name="userrssitemmodel",
            old_name="user_rss",
            new_name="following_rss",
        ),
    ]