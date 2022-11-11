from django.contrib import admin

from .models import RSSItemModel, RSSModel, UserRSSItemModel, UserRSSModel


# Register your models here.
@admin.register(RSSModel)
class RSSModelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "ttl",
        "created_at",
        "updated_at",
    )
    fields = ("link",)

    # def save_model(self, request, obj, form, change):


@admin.register(RSSItemModel)
class RSSItemModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRSSModel)
class UserRSSModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRSSItemModel)
class UserRSSItemModelAdmin(admin.ModelAdmin):
    pass
