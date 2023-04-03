from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Activity, ActivityLog, Tip, MeterReading, Award, Faction, Location, Challenger, Riddle

# Test for each model that was created in models.py
class CategoryModelTest(TestCase):

    def test_category_creation(self):
        category = Category.objects.create(name="Fitness")
        self.assertEqual(str(category), "Fitness")
        
class ActivityModelTest(TestCase):

    def test_activity_creation(self):
        category = Category.objects.create(name="Fitness")
        activity = Activity.objects.create(title="Run for 30 minutes", points=50, cat=category)
        self.assertEqual(str(activity), "Run for 30 minutes")
        
class ActivityLogModelTest(TestCase):

    def test_activity_log_creation(self):
        user = User.objects.create(username="alice")
        category = Category.objects.create(name="Fitness")
        activity = Activity.objects.create(title="Run for 30 minutes", points=50, cat=category)
        activity_log = ActivityLog.objects.create(date="2023-04-01", challenger=user)
        activity_log.activities.add(activity)
        self.assertEqual(str(activity_log), "Activity Log for alice on 2023-04-01")
        
class TipModelTest(TestCase):

    def test_tip_creation(self):
        tip = Tip.objects.create(description="Drink plenty of water")
        self.assertEqual(str(tip), "Drink plenty of water")
        
class MeterReadingModelTest(TestCase):

    def test_meter_reading_creation(self):
        user = User.objects.create(username="alice")
        meter_reading = MeterReading.objects.create(value=100, challenger=user)
        self.assertEqual(str(meter_reading), "Meter Reading #1")
        
class AwardModelTest(TestCase):

    def test_award_creation(self):
        user = User.objects.create(username="alice")
        award = Award.objects.create(title="Most Improved Challenger", challenger=user)
        self.assertEqual(str(award), "Most Improved Challenger")
        
class FactionModelTest(TestCase):

    def test_faction_creation(self):
        user = User.objects.create(username="alice")
        faction = Faction.objects.create(score=100, challenger=user)
        self.assertEqual(str(faction), "Faction #1")
        
class LocationModelTest(TestCase):

    def test_location_creation(self):
        category = Category.objects.create(name="Fitness")
        faction = Faction.objects.create(score=100, challenger=User.objects.create(username="alice"))
        location = Location.objects.create(postcode="SW1A 1AA", country="UK", size_squ_ft=1000, faction=faction)
        self.assertEqual(str(location), "SW1A 1AA")
        
class ChallengerModelTest(TestCase):

    def test_challenger_creation(self):
        user = User.objects.create(username="alice")
        challenger = Challenger.objects.create(user=user, score=100, postcode="SW1A 1AA")
        self.assertEqual(str(challenger), "alice (SW1A 1AA)")
        
class RiddleModelTest(TestCase):

    def test_riddle_creation(self):
        riddle = Riddle.objects.create(text="What has a head and a tail, but no body?")
        self.assertEqual(str(riddle), "Riddle 1: What has a head and a tail, but no body?")