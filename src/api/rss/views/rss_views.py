from django.db.models.query import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import exceptions, generics, permissions, response
from rest_framework.request import Request
from rss.models import RSSModel
from rss.serializers import RSSSerializer, UserRssFollowingRequest
from utils import to_bool


class UserRSSView(generics.ListAPIView):
    queryset = RSSModel.objects.all()
    serializer_class = RSSSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def filter_queryset(self, queryset: QuerySet):
        filter_by_user = to_bool(self.request.query_params.get("following"))
        if filter_by_user:
            queryset = queryset.filter(users=self.request.user)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="following",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter following rss",
                examples=[
                    OpenApiExample(
                        "Show only following rss", summary="Filter following rss", value=True
                    ),
                    OpenApiExample("Get all rss feeds", summary="Get all rss feeds", value=False),
                ],
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserRSSFollowingView(generics.GenericAPIView):
    queryset = RSSModel.objects.all()
    serializer_class = UserRssFollowingRequest
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs):
        rss_model = self.get_object()
        rss_model.users.add(self.request.user)
        return response.Response(status=201)

    def delete(self, request: Request):
        rss_model = self.get_object()
        rss_model.users.remove(self.request.user)
        return response.Response(status=204)

    def _get_rss_feed_id(self):
        serializer = UserRssFollowingRequest(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["id"]

    def get_object(self) -> RSSModel:
        rss_feed_id = self._get_rss_feed_id()
        try:
            return RSSModel.objects.get(pk=rss_feed_id)
        except RSSModel.DoesNotExist:
            raise exceptions.NotFound(detail=f"RSS feed {rss_feed_id} does not exist")


class ForceRssUpdate(generics.GenericAPIView):
    def post(self):
        pass
