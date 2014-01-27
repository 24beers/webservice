from django.conf.urls import patterns, url, include
from django.contrib import admin
from rest_framework import routers
from endpoint.views import GroupViewSet, UserViewSet, PairViewSet, RegisterView

admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'pairs', PairViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^admin/', include(admin.site.urls)),
                       #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^register/', RegisterView().register)
)