from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_private_cars(self):
        driver_one = get_user_model().objects.create(
            license_number="ASD12345",
            username="test1",
            first_name="John1",
            last_name="Doe1",
        )
        driver_two = get_user_model().objects.create(
            license_number="ASD54321",
            username="test2",
            first_name="John2",
            last_name="Doe2",
        )
        manufacturer = Manufacturer.objects.create(name="test", country="US")
        car = Car(model="test", manufacturer=manufacturer, id=1)
        car.drivers.add(driver_one)
        car.drivers.add(driver_two)
        car.save()
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars),
        )

    def test_private_driver(self):
        Driver.objects.create(
            license_number="ASD12345",
            username="user2",
        )
        Driver.objects.create(
            license_number="ASD54321",
            username="user1",
        )
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers),
        )

    def test_private_manufacturers(self):
        Manufacturer.objects.create(name="test", country="US")
        Manufacturer.objects.create(name="test123", country="US123")
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers),
        )
