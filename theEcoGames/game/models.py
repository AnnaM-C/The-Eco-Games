from django.db import models
from django.contrib.auth.models import User

class Points(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)

    def __str__(self):
        return self.title

    class PointsChoices(models.Model):
        ten=10
        twenty=20
        thirty=30
        forty=40
        fifty=50


class ActivityList(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    title = models.TextField(max_length=128, unique=True)
    points = models.ForeignKey(Points, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Activity(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True)
    date=models.DateTimeField(auto_now_add=True)
    activityList=models.ForeignKey(ActivityList, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Tip(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True)
    description=models.TextField(max_length=500)

    def __str__(self):
        return self.title

class MeterReading(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True)
    value=models.CharField(max_length=128)

    def __str__(self):
        return self.title

class Award(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True)
    title=models.TextField(max_length=128)

    def __str__(self):
        return self.title

class Location(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True)
    postcode=models.CharField(max_length=128)
    country=models.TextField(max_length=128)
    size_squ_ft=models.CharField(max_length=128)

    def __str__(self):
        return self.title

class Faction(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True)
    score=models.CharField(max_length=128)
    location=models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Many-to-many class. User logs many activities in an associative table
class UserActivity(models.Model):
    user_x=models.ForeignKey(User, on_delete=models.CASCADE)
    activity_x=models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Many-to-many class. User logs many tips in an associative table
class UserTip(models.Model):
    user_x=models.ForeignKey(User, on_delete=models.CASCADE)
    tip_x=models.ForeignKey(Tip, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Challenger(models.Model):
    #id = models.BigAutoField(auto_created=True, primary_key=True)
    userlink = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=128, unique=True)
    score = models.CharField(max_length=128) # FIX THIS!!!!!!!!!!!!
    activity_user = models.ForeignKey(UserActivity, on_delete=models.CASCADE)
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    meter_reading=models.ForeignKey(MeterReading, on_delete=models.CASCADE)
    award=models.ForeignKey(Award, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


