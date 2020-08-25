from django.conf.urls import url

from rest_framework import routers

from build_migration.users import views

app_name = "users"
router = routers.DefaultRouter()
router.register("", views.UserViewSet)
urlpatterns = router.urls
