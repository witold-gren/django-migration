from django.conf import settings

import factory


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user-{n}")
    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ("username",)
