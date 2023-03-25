from django.contrib.auth.models import Group
from .factories import *
from django.db import transaction

#@transaction.atomic
#from django_seed import Seed

#seeder = Seed.seeder()



#inserted_pks = seeder.execute()
def seed():
    
    try:
        with transaction.atomic():
            groupOwner = GroupFactory.create(name="shop-owner")
            groupBot = GroupFactory.create(name="bot")

            # Create superusers
            superuser1 = SuperuserFactory.create(
                username="admin",
                email="admin@example.com",
                password="password",
            )
            superuser1.groups.set([groupOwner])

            botuser1 = UserFactory.create(
                username="bot",
                email="bot@example.com",
                password="password",
            )
            botuser1.groups.set([groupBot])

            for _ in range(5):
                user = UserFactory.create(
                    password="password"
                )
                user.groups.set([groupOwner])
            for _ in range(10):
                user = UserFactory.create(
                    password="password"
                )

            for _ in range(5):
                shop = ShopFactory.create()

            ProductTypeFactory.create(name='vegetables', )

            for _ in range(10):
                ProductFactory.create()

            # purchases = []
            # for _ in range(5):
            #     purchase = PurchaseFactory.create()
            #     purchase.update_total_price()
                
            

            

        print('Data seeded successfully.')
    except Exception as e:
        print('Error seeding data:', str(e))
        raise e