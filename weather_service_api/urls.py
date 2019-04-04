from django.urls import include, path
from rest_framework import routers
from weather.views import user_view, group_view
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

schema_view = get_swagger_view(title='Weather API')

router = routers.DefaultRouter()
router.register(r'users', user_view.UserViewSet)
router.register(r'groups', group_view.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include('weather.urls')),
    path('swagger-docs/', schema_view),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', include_docs_urls(title='My API title')),
]


