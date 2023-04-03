from django.core.management.base import BaseCommand 
from game.models import *

class Command(BaseCommand):

    def handle(self, *args, **options): 

        Activity.objects.all().delete()

        #seed activities
        c=Category(name="Home")
        c.save()
        n=Activity(title="Showered for 2 minutes", points=10, cat=c) 
        n.save()

        n=Activity(title="Turned down heating", points=10, cat=c) 
        n.save()

        n=Activity(title="Washing", points=10, cat=c) 
        n.save()

        n=Activity(title="Showered for 5 minutes", points=10, cat=c) 
        n.save()

        n=Activity(title="Showered for 1 minute", points=10, cat=c) 
        n.save()
        self.stdout.write('done.')

        Riddles.objects.all().delete()

        # seed riddles

        r=Riddles(text="Welcome to the Eco Games! Every month you will see a new riddle. Here's one to get you started.. I touch your face, I'm in your words, I'm lack of space and beloved by birds")
        r.save()