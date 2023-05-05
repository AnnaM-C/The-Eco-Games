from django.test import  Client, TestCase
from .models import Challenger, Category, Activity, UserCart, LineItem, Tip, MeterReading, Award, Faction, Location, UserTip, Riddles
from django.contrib.auth.models import User
from django.urls import reverse
from game.views import *
from unittest.mock import patch, MagicMock

class ChallengerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        Challenger.objects.create(user=user, score=100, postcode='AB1C')

    def test_str(self):
        challenger = Challenger.objects.get(id=1)
        self.assertEqual(str(challenger), challenger.user.username)


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category')

    def test_str(self):
        category = Category.objects.get(id=1)
        self.assertEqual(str(category), category.name)


class ActivityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Test Category')
        Activity.objects.create(title='Test Activity', points=10, cat=category)

    def test_str(self):
        activity = Activity.objects.get(id=1)
        self.assertEqual(str(activity), activity.title)


class UserCartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        challenger = Challenger.objects.create(user=user, score=100, postcode='AB1C')
        UserCart.objects.create(challenger=challenger)

    def test_str(self):
        cart = UserCart.objects.get(id=1)
        self.assertEqual(str(cart), cart.challenger.user.username)


class LineItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        challenger = Challenger.objects.create(user=user, score=100, postcode='AB1C')
        category = Category.objects.create(name='Test Category')
        activity = Activity.objects.create(title='Test Activity', points=10, cat=category)
        cart = UserCart.objects.create(challenger=challenger)
        LineItem.objects.create(timeRecorded='10:00:00', dateRecorded='2022-01-01', activityDuration=30, checkedOut=False, activity=activity, cart=cart)

    def test_str(self):
        item = LineItem.objects.get(id=1)
        self.assertEqual(str(item), item.activity.title)

class TipModelTest(TestCase):
    def setUp(self):
        Tip.objects.create(description='This is a test tip.')
        Tip.objects.create(description='Another test tip.')

    def test_tip_description(self):
        tip1 = Tip.objects.get(description='This is a test tip.')
        tip2 = Tip.objects.get(description='Another test tip.')
        self.assertEqual(tip1.description, 'This is a test tip.')
        self.assertEqual(tip2.description, 'Another test tip.')

class UserTipModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.tip1 = Tip.objects.create(description='This is a test tip.')
        self.tip2 = Tip.objects.create(description='Another test tip.')
        self.usertip = UserTip.objects.create(challenger=self.user)

    def test_user_tip_relationship(self):
        self.usertip.tip.add(self.tip1)
        self.assertEqual(self.usertip.tip.count(), 1)
        self.usertip.tip.add(self.tip2)
        self.assertEqual(self.usertip.tip.count(), 2)

    def test_user_tip_challenger(self):
        usertip = UserTip.objects.get(challenger=self.user)
        self.assertEqual(usertip.challenger, self.user)


class MeterReadingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        MeterReading.objects.create(value='Test Value', challeger=user)

    def test_str(self):
        reading = MeterReading.objects.get(id=1)
        self.assertEqual(str(reading), reading.value)


class AwardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        challenger = Challenger.objects.create(user=user, score=100, postcode='AB1C')
        Award.objects.create(title='Test Award', challenger=user)

    def test_str(self):
        award = Award.objects.get(id=1)
        self.assertEqual(str(award), award.title)


class FactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.challenger = Challenger.objects.create(user=self.user)
        self.faction = Faction.objects.create(score=100, challenger=self.user)

    def test_faction_score(self):
        self.assertEqual(self.faction.score, '100')
                        
class LocationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.challenger = Challenger.objects.create(user=self.user)
        self.faction = Faction.objects.create(score=100, challenger=self.user)
        self.location = Location.objects.create(postcode='12345', country='Test Country', size_squ_ft='1000', faction=self.faction)

    def test_location_postcode(self):
        self.assertEqual(self.location.postcode, '12345')
        


class GameViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.challenger = Challenger.objects.create(user=self.user, score=0)

    