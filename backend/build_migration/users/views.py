from django.contrib.auth import get_user_model

from rest_framework import status, viewsets

from build_migration.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
