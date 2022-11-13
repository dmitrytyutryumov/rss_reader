from rest_framework import serializers
from rss.models import RSSItemModel, RSSModel


class RSSSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = RSSModel
        exclude = (
            "created_at",
            "updated_at",
            "users",
        )

    def get_following(self, obj):
        current_user = self.context["request"].user
        if obj.userrssmodel_set.filter(user=current_user).exists():
            return True
        return False


class RSSItemSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = RSSItemModel
        exclude = ("user_rss",)

    def get_is_read(self, obj: RSSItemModel):
        current_user = self.context["request"].user
        if obj.userrssitemmodel_set.filter(following_rss__user=current_user).exists():
            return True
        return False


class UserRssFollowingRequest(serializers.Serializer):
    id = serializers.IntegerField(required=True)


class MarkRSSItemSerializer(serializers.Serializer):
    rss_id = serializers.IntegerField(required=True)


class ForceUpdateRSSSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
