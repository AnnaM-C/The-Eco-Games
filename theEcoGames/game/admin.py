from django.contrib import admin
from .models import Points, ActivityList, Activity, Tip, MeterReading, Award, Location, Faction, User, UserActivity, UserTip

# Register your models here.

admin.site.register(Points)
admin.site.register(ActivityList)
admin.site.register(Activity)
admin.site.register(Tip)
admin.site.register(MeterReading)
admin.site.register(Award)
admin.site.register(Location)
admin.site.register(Faction)

admin.site.register(UserActivity)
admin.site.register(UserTip)

# Register your models here.
