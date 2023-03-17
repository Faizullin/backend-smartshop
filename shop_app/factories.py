import factory
from django.contrib.auth.models import Group
from django.utils import timezone
from .models import Shop, Product, ProductType, CustomUser, Purchase, PurchaseItem
from django.core.files.uploadedfile import SimpleUploadedFile

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"group{n}")
    
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)
    password = factory.PostGenerationMethodCall('set_password',
                                                'defaultpassword')


class SuperuserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop
    name = factory.Sequence(lambda n: 'Shop {}'.format(n))
    owner = factory.SubFactory(UserFactory)
    address = factory.Sequence(lambda n: 'shop-{}-address'.format(n))
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: 'Product Type {}'.format(n))
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    description = factory.Faker('paragraph')
    # image = factory.django.ImageField(
    #     width=800,
    #     height=800,
    #     color='blue',
    #     filename=factory.Sequence(lambda n: f'product_{n}.jpg')
    # )
    shop = factory.SubFactory(ShopFactory)
    type = factory.SubFactory(ProductTypeFactory)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

class PurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Purchase
    
    status = 'PENDING'
    total_price = 0
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    # @factory.post_generation
    # def items(self, create, extracted, **kwargs):
    #     if not create:
    #         return

    #     if extracted:
    #         for item in extracted:
    #             self.items.add(item)
    #     else:
    #         PurchaseItemFactory.create_batch(3, purchase=self)
    #         self.update_total_price()

    # def update_total_price(self):
    #     self.total_price = sum(item.price * item.quantity for item in self.items.all())
    #     self.save()
    

class PurchaseItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseItem
    
    purchase = factory.SubFactory(PurchaseFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('pyint', min_value=1, max_value=10)
    price = factory.Faker('pyint', min_value=1, max_value=10)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

