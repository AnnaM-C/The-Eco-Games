from django.core.management.base import BaseCommand 
from game.models import *

class Command(BaseCommand):

    def handle(self, *args, **options): 

        Activity.objects.all().delete()
        Category.objects.all().delete()
        Location.objects.all().delete()

        # # Seed users

        user34 = User(username='user34', email='user34@surrey.ac.uk') 
        user34.set_password('MyPassword123')
        user34.save()
        challenger34=Challenger(user=user34, score=3332, postcode="YO5")
        challenger34.save()

        user35 = User(username='user35', email='user35@surrey.ac.uk') 
        user35.set_password('MyPassword123')
        user35.save()
        challenger35=Challenger(user=user35, score=2121, postcode="BT5")
        challenger35.save()

        user36 = User(username='user36', email='user36@surrey.ac.uk') 
        user36.set_password('MyPassword123')
        user36.save()
        challenger36=Challenger(user=user36, score=9239, postcode="DN1")
        challenger36.save()

        user37 = User(username='user37', email='user37@surrey.ac.uk') 
        user37.set_password('MyPassword123')
        user37.save()
        challenger37=Challenger(user=user37, score=10059, postcode="NG4")
        challenger37.save()

        user38 = User(username='user38', email='user38@surrey.ac.uk') 
        user38.set_password('MyPassword123')
        user38.save()
        challenger38=Challenger(user=user38, score=1835, postcode="HS1")
        challenger38.save()

        user39 = User(username='user39', email='user39@surrey.ac.uk') 
        user39.set_password('MyPassword123')
        user39.save()
        challenger39=Challenger(user=user39, score=402, postcode="TA1")
        challenger39.save()

        # Seed Categories
        c1=Category(name="Kitchen")
        c1.save()
        c2=Category(name="Bathroom")
        c2.save()
        c3=Category(name="Rooms")
        c3.save()
        c4=Category(name="Electronics")
        c4.save()
        c5=Category(name="Washing")
        c5.save()
        c6=Category(name="Heating")
        c6.save()

        

        #seed activities
        # Kitchen
        n = Activity(title="Use lids on pots and pans while cooking", points=10, cat=c1)
        n.save()
        n = Activity(title="Use a microwave or toaster oven instead of a regular oven", points=10, cat=c1)
        n.save()
        n = Activity(title="Composte food waste instead of throwing it away", points=10, cat=c1)
        n.save()        
        n = Activity(title="Use a reusable water bottle instead of disposable plastic bottles", points=10, cat=c1)
        n.save()
        n = Activity(title="Use a hybrid or electric vehicle", points=10, cat=c1)
        n.save()
        n = Activity(title="Use a ceiling fan to cool home instead of air conditioning", points=10, cat=c1)
        n.save()
        
        
        # Bathroom
        n = Activity(title="Take a shorter shower", points=10, cat=c2, type=Activity.ActivityType.TIMEREQUIRED)
        n.save()        
        n = Activity(title="Use a low-flow showerhead", points=10, cat=c2, type=Activity.ActivityType.TIMENOTREQUIRED)
        n.save()
        n = Activity(title="Fix leaky faucets and toilets promptly", points=10, cat=c2)
        n.save()
        n = Activity(title="Turn off the water when brushing teeth or shaving", points=10, cat=c2)
        n.save()
        n = Activity(title="Use a water-saving toilet", points=10, cat=c2)
        n.save()
        n = Activity(title="Use natural cleaning products instead of harsh chemicals", points=10, cat=c2)

        # Room
        n = Activity(title="Close curtains and blinds to keep heat out in the summer and retain heat in the winter", points=10, cat=c3)
        n.save()
        n = Activity(title="Use LED light bulbs instead of incandescent bulbs", points=10, cat=c3)
        n.save()
        n = Activity(title="Turn off lights when leaving a room", points=10, cat=c3)
        n.save()
        n = Activity(title="Clean filters in heating and cooling systems", points=10, cat=c3)
        n.save()
        n = Activity(title="Seal gaps and cracks in doors and windows to prevent air leaks", points=10, cat=c3)
        n.save()
        n = Activity(title="Use weather stripping around doors and windows", points=10, cat=c3)
        n.save()
        n = Activity(title="Use natural light instead of electric lighting during the day", points=10, cat=c3)
        n.save()

        # Electronics
        n = Activity(title="Unplug electronics when not in use", points=10, cat=c4)
        n.save()
        n = Activity(title="Use a power strip to turn off electronics when not in use", points=10, cat=c4)
        n.save()
        n = Activity(title="Use the energy-saving mode on appliances like washing machines and dishwashers", points=10, cat=c4)
        n.save()
        n = Activity(title="Use rechargeable batteries", points=10, cat=c4)
        n.save()
        n = Activity(title="Use a laptop instead of a desktop computer", points=10, cat=c4)
        n.save()
        n = Activity(title="Use a fan instead of air conditioning on mild days", points=10, cat=c4)
        n.save()
        n = Activity(title="Use a power-saving mode on your computer or other devices", points=10, cat=c4)
        n.save()

        # Washing
        n = Activity(title="Air-dry clothes instead of using a dryer", points=10, cat=c5)
        n.save()
        n = Activity(title="Clean the lint filter in the dryer", points=10, cat=c5)
        n.save()
        n = Activity(title="Wash laundry in cold water", points=10, cat=c5)
        n.save()

        # Heating
        n = Activity(title="Turn down the thermostat", points=10, cat=c6)
        n.save()
        n = Activity(title="Replace inefficient boiler", points=10, cat=c6)
        n.save()
        n = Activity(title="Tackle draughty spots", points=10, cat=c6)
        n.save()
        n = Activity(title="Lower water temperature", points=10, cat=c6)
        n.save()
        n = Activity(title="Set boiler timer so hot water is not heated all day", points=10, cat=c6)
        n.save()


        self.stdout.write('done.')

        Riddles.objects.all().delete()

        # seed riddles

        r=Riddles(text="Welcome to the Eco Games! Every month you will see a new riddle. Here's one to get you started.. I am in your words, I am lack of space and beloved by birds")
        r.save()



        # Activities that require a time
        # Showering
        # Washing machine
        

        # Activities that require miles
        # Driving

        # Activities that require degrees
        # Turn down thermostat


# Daily activities (Little points)
        # Have a shower -> input duration
        # Use the microwave instead of oven
        # Hang washing instead of using tumble dryer
        # Wash clothes in cold water instead of hot
        # Turn the heating down -> input degrees
        # Turn TV's onto standby
        # Use full load dishwasher
        # Blocked draughts

        # Switch off standby

        # For meals: use a slow cooker: they use basically the same energy as a light bulb.


# Weekly activities



# One-off energy saving activities (Mega points)
        # Insulate the loft
        # Insulate boiler
        # Add solar panels
        # Change your gas hob to an electric hob
        # Install LED lights
        # Install a Qwokka instead of using a kettle
        # Bleed your radiator


# Reminders
        # Keep tap off whilst brushing teeth
        # Recycle bins
        # Turn off the lights
        # Avoid overfilling kettle
        # Avoid the tumble dryer hang your washing
        # For meals: Microwave a leftover meal instead of using the oven to cook something
        # Used glass/ceramic pans they retain heat better than metal
        # Dont heat empty rooms
        # Close curtains