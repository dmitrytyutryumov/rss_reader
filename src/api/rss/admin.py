from django.contrib import admin

from .models import RSSItemModel, RSSModel, UserRSSItemModel, UserRSSModel


# Register your models here.
@admin.register(RSSModel)
class RSSModelAdmin(admin.ModelAdmin):
    pass


@admin.register(RSSItemModel)
class RSSItemModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRSSModel)
class UserRSSModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRSSItemModel)
class UserRSSItemModelAdmin(admin.ModelAdmin):
    pass
