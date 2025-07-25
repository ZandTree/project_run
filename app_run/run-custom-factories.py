# from datetime import datetime

# import factory
# from django.contrib.auth.models import User
# from factory.django import DjangoModelFactory
# from faker import Faker

# from .models import Run

# faker = Faker()


# class UserFactory(DjangoModelFactory):
#     class Meta:
#         model = User
#         django_get_or_create = ("username", "email")

#     username = factory.Sequence(lambda n: f"user-{n}")
#     email = factory.LazyAttribute(lambda _: faker.unique.email())
#     password = factory.PostGenerationMethodCall("set_password", "12345abc")
#     first_name = factory.Faker('first_name')
#     last_name = factory.Faker('last_name')
#     date_joined = factory.LazyFunction(datetime.now)
    
    
    

# class RunFactory(DjangoModelFactory):
#     class Meta:
#         model = Run       
#     comment = factory.Faker("word") 
#     athlete = factory.SubFactory(UserFactory)
#     created_at = factory.LazyFunction(datetime.now)


