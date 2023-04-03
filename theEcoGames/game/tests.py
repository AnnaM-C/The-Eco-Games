from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from game.models import Activity, Location, ActivityList, UserActivity, Award, MeterReading
# Create your tests here.


class MeterReadingTestCase(TestCase):
    def test_meter_reading_creation(self):
        #Test creating a new MeterReading
        value = Decimal('100.00')
        reading = MeterReading.objects.create(value=value)
        self.assertTrue(isinstance(reading, MeterReading))
        self.assertEqual(reading.value, value)
        
class LocationTest(TestCase):
    def test_create_location(self):
        # Create a new location
        Location.objects.create(
            id="1234",
            postcode="GU2 7XY",
            country=-73.968285,
            size_squ_ft=100,
        )
        
class ActivityTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            date="2023-03-25",
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.id, 1)
        self.assertEqual(str(self.activity.date), "2022-03-25")

class ActivityListTest(TestCase):
    def setUp(self):
        self.activity_list = ActivityList.objects.create(
            title="Weekend activities",
        )
        self.activity1 = Activity.objects.create(
            name="Hiking",
            points=10,
            activity_list=self.activity_list
        )
        self.activity2 = Activity.objects.create(
            name="Biking",
            points=5,
            activity_list=self.activity_list
        )

    def test_activity_list_creation(self):
        self.assertEqual(self.activity_list.id, 1)
        self.assertEqual(self.activity_list.title, "Weekend activities")
        self.assertEqual(self.activity_list.description, "Turn off lights that aren't in use")

    def test_activity_creation(self):
        self.assertEqual(self.activity1.id, 1)
        self.assertEqual(self.activity1.name, "Hiking")
        self.assertEqual(self.activity1.points, 10)
        self.assertEqual(self.activity1.activity_list, self.activity_list)

        self.assertEqual(self.activity2.id, 2)
        self.assertEqual(self.activity2.name, "Biking")
        self.assertEqual(self.activity2.points, 5)
        self.assertEqual(self.activity2.activity_list, self.activity_list)
        
class UserActivityTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def test_useractivity_model(self):
        useractivity = UserActivity.objects.create(user_x=self.user, activity_x='Test Activity')
        self.assertEqual(useractivity.user_x, self.user)
        self.assertEqual(useractivity.activity_x, 'Test Activity')
        self.assertEqual(str(useractivity), 'testuser - Test Activity')
        
class AwardTest(TestCase):
    def test_award_model(self):
        award = Award.objects.create(title='Test Award')
        self.assertEqual(award.title, 'Test Award')
        self.assertEqual(str(award), 'Test Award')
        
