from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

import schedule.views as sv

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()
app_router.register(
    "setup", sv.SetupViewSet, "setup"
)

urlpatterns = [
    path("", include(app_router.urls)),
]
