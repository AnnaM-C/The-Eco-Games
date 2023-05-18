from django.db import models
from django.contrib.auth.models import User


class Challenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    postcode=models.CharField(max_length=4)
    
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name=models.CharField(max_length=128)
    def __str__(self):
        return self.name


class Activity(models.Model):
    title = models.TextField(max_length=128, unique=True)
    points=models.IntegerField()
    cat=models.ForeignKey(Category, on_delete=models.CASCADE)

    class ActivityType(models.TextChoices):
        TIMEREQUIRED = 'TR', ('Time required')
        TIMENOTREQUIRED = 'TNR', ('Time not required')

    type=models.CharField(max_length=4, default=ActivityType.TIMENOTREQUIRED)

    def __str__(self):
        return self.title

class UserCart(models.Model):
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    challenger=models.ForeignKey(Challenger, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.challenger.user.username

class LineItem(models.Model):
    timeRecorded=models.TimeField()
    dateRecorded=models.DateField()
    activityDuration=models.IntegerField(default=0)
    checkedOut=models.BooleanField(default=False)
    activity=models.ForeignKey(Activity, on_delete=models.CASCADE)
    cart=models.ForeignKey(UserCart, on_delete=models.CASCADE)

    def __str__(self):
        return self.activity.title

class Tip(models.Model):
    description=models.TextField(max_length=500)

class MeterReading(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True)
    value=models.CharField(max_length=128)
    challeger=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.value

class Award(models.Model):
    title=models.TextField(max_length=128)
    challenger=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    
class Faction(models.Model):
    score=models.CharField(max_length=128)
    challenger=models.ForeignKey(User, on_delete=models.CASCADE)


class Location(models.Model):
    postcode=models.CharField(max_length=128)
    country=models.TextField(max_length=128)
    size_squ_ft=models.CharField(max_length=128)
    # faction=models.ForeignKey(Faction, on_delete=models.CASCADE)
    score=models.IntegerField(default=0)

    def __str__(self):
        return self.postcode



# Many-to-many class. User logs many tips in an associative table
class UserTip(models.Model):
    challenger=models.ForeignKey(User, on_delete=models.CASCADE)
    tip=models.ManyToManyField(Tip)


class Riddles(models.Model):
    r_id=models.IntegerField(default=1)
    text=models.TextField()

