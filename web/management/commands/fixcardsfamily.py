from django.core.management.base import BaseCommand, CommandError
from web import models

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        cards = models.Card.objects.filter(parent__isnull=False)
        for card in cards:
            card.rarity = card.parent.rarity
            card.performer = card.parent.performer
            card.attributes = card.parent.attributes
            card.save()
            print "Updated {}".format(card)
