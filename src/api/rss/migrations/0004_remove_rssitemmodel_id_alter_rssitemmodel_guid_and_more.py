# Generated by Django 4.1.3 on 2022-11-11 16:42

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rss", "0003_remove_rssmodel_copyright_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rssitemmodel",
            name="id",
        ),
        migrations.AlterField(
            model_name="rssitemmodel",
            name="guid",
            field=models.CharField(max_length=300, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name="rssitemmodel",
            name="last_updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="rssmodel",
            name="link",
            field=models.URLField(unique=True, verbose_name="RSS source link"),
        ),
        migrations.AlterField(
            model_name="rssmodel",
            name="updated_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterIndexTogether(
            name="userrssitemmodel",
            index_together={("following_rss", "rss_item")},
        ),
        migrations.AlterIndexTogether(
            name="userrssmodel",
            index_together={("user", "rss")},
        ),
    ]
