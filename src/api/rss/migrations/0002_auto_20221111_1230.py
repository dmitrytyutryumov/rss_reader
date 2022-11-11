from django.db import migrations

RSS_DEFAULT_SOURCES = {
    "Algemeen": "http://www.nu.nl/rss/Algemeen",
    "Tweakers": "https://feeds.feedburner.com/tweakers/mixed",
    "Cnn": "http://rss.cnn.com/rss/edition.rss",
}


def forwards_func(apps, schema_editor):
    RSSModel = apps.get_model("rss", "RSSModel")
    db_alias = schema_editor.connection.alias
    RSSModel.objects.using(db_alias).bulk_create(
        [RSSModel(title=title, link=link) for title, link in RSS_DEFAULT_SOURCES.items()]
    )


def reverse_func(apps, schema_editor):
    RSSModel = apps.get_model("rss", "RSSModel")
    db_alias = schema_editor.connection.alias
    RSSModel.objects.using(db_alias).filter(link__in=RSS_DEFAULT_SOURCES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("rss", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
