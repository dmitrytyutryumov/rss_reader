from django.db.models.query import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import exceptions, generics, permissions, response
from rest_framework.request import Request
from rss.models import RSSItemModel
from rss.serializers import MarkRSSItemSerializer, RSSItemSerializer
from utils import to_bool


class UserRSSItemView(generics.ListAPIView):
    queryset = RSSItemModel.objects.all()
    serializer_class = RSSItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        rss_feed_id = self.request.query_params.get("rss")
        if rss_feed_id:
            queryset = queryset.filter(rss__id=rss_feed_id)

        is_read = self.request.query_params.get("is_read")
        if is_read is not None:
            if to_bool(is_read):
                queryset = queryset.filter(userrssitemmodel__id__isnull=False)
            else:
                queryset = queryset.filter(userrssitemmodel__id__isnull=True)
        return queryset.filter(rss__users=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="rss",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter items by given rss id",
                examples=[
                    OpenApiExample(
                        "Show items only for chosen rss feed",
                    ),
                ],
            ),
            OpenApiParameter(
                name="is_read",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter read / unread items",
                examples=[
                    OpenApiExample("Show read items", value=True),
                    OpenApiExample("Show unread items", value=False),
                ],
            ),
        ],
    )
    def get(self, request: Request, *args, **kwargs) -> response.Response:
        return super().get(request, *args, **kwargs)


class UserReadRSSItemView(generics.GenericAPIView):
    queryset = RSSItemModel.objects.all()
    serializer_class = MarkRSSItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> response.Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        rss_item = self.get_object()
        try:
            following_rss = rss_item.rss.userrssmodel_set.get(user=self.request.user)
            rss_item.user_rss.add(following_rss)
            return response.Response(status=201)
        except rss_item.user_rss.model.DoesNotExist:
            raise exceptions.NotFound("User does not follow rss feed.")

    def delete(self, request: Request, *args, **kwargs) -> response.Response:
        rss_item = self.get_object()
        rss_item.userrssitemmodel_set.filter(following_rss__user=self.request.user).delete()
        return response.Response(status=204)
