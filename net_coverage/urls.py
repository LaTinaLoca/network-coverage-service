from django.urls import include, path
from rest_framework import routers
from net_coverage import views

router = routers.DefaultRouter()

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/get-network-coverage/', views.GetNetworkCoverage.as_view(), name='get-network-coverage'),
]