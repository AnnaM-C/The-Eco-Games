from django.db import models
from django.contrib.auth.models import User

# class Points(models.Model):
#     # choices = [
#     #     ('ten',10),
#     #     ('twenty',20),
#     #     ('thirty',30),
#     #     ('forty',40),
#     #     ('fifty',50),
#     # ]
#     choices=models.IntegerField()
#     def __str__(self):
#         return self.title
    


class Activity(models.Model):
    title = models.TextField(max_length=128, unique=True)
    points=models.IntegerField()

    # def __str__(self):
    #     return self.title


class ActivityLog(models.Model):
    date=models.DateField()
    challenger=models.ForeignKey(User, on_delete=models.CASCADE)
    activities=models.ManyToManyField(Activity)

    
# Many-to-many class. User logs many activities in an associative table
# class ManyToManyTable_ActivityForm(models.Model):
#     challenger=models.ForeignKey(User, on_delete=models.CASCADE)
#     date=models.DateField()
#     # activity_log=models.ForeignKey(ActivityLog, on_delete=models.CASCADE)
#     activityList=models.ForeignKey(ActivityChoices, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title

class Tip(models.Model):
    description=models.TextField(max_length=500)

class MeterReading(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True)
    value=models.CharField(max_length=128)
    challeger=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
    faction=models.ForeignKey(Faction, on_delete=models.CASCADE)


# Many-to-many class. User logs many tips in an associative table
class UserTip(models.Model):
    challenger=models.ForeignKey(User, on_delete=models.CASCADE)
    tip=models.ManyToManyField(Tip)



class Challenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0) # FIX THIS!!!!!!!!!!!!


class Riddles(models.Model):
    r_id=models.IntegerField(default=1)
    text=models.TextField()

