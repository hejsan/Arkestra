import operator

from datetime import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings

MULTIPLE_ENTITY_MODE = settings.MULTIPLE_ENTITY_MODE

class ArkestraGenericModelManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def get_items(self, instance):
        publishable_items = self.get_publishable_items(instance)        
        if instance.order_by == "importance/date":
            top_items, ordinary_items = self.get_items_ordered_by_importance_and_date(instance, publishable_items)
            return  top_items + ordinary_items
        else:
            return self.get_publishable_items(instance)

    def get_publishable_items(self, instance):
        # returns items that can be published, latest items first
        publishable_items = self.get_items_for_entity(instance) \
            .filter(date__lte = datetime.today(), published=True, in_lists=True) \
            .order_by('-date')
        return publishable_items

    def get_items_for_entity(self, instance):
        # returns every items item associated with this entity, 
        # or all items items if MULTIPLE_ENTITY_MODE is False, or instance.entity is unspecified
        if MULTIPLE_ENTITY_MODE and instance.entity:
            items_for_entity = self.model.objects.filter(
                Q(hosted_by=instance.entity) | Q(publish_to=instance.entity)
                ).distinct()
        else:
            items_for_entity = self.model.objects.all()
        # print "All items", all_items.count()
        return items_for_entity

    def get_items_ordered_by_importance_and_date(self, instance, publishable_items):
        ordinary_items = []

        # split the within-date items for this entity into two sets
        publishable_items = self.get_publishable_items(instance)
        sticky_items = publishable_items.order_by('-importance').filter(
            Q(hosted_by=instance.entity) | Q(is_sticky_everywhere = True),
            sticky_until__gte=datetime.today(),  
            )
        non_sticky_items = publishable_items.exclude(
            Q(hosted_by=instance.entity) | Q(is_sticky_everywhere = True),
            sticky_until__gte=datetime.today(), 
            )
        # print "Sticky items", sticky_items.count()
        # print "Non-sticky items", non_sticky_items.count()
        top_items = list(sticky_items)

        # now we have to go through the non-top items, and find any that can be promoted
        # get the set of dates where possible promotable items can be found             
        dates = non_sticky_items.dates('date', 'day').reverse()
        # print "Going through the date set"
        for date in dates:
            # print "    examining possibles from", date
            # get all non-top items from this date
            possible_top_items = non_sticky_items.filter(date__year=date.year, date__month= date.month, date__day= date.day)
            # promotable items have importance > 0
            # print "        found", possible_top_items.count(), "of which I will promote", possible_top_items.filter(Q(hosted_by=instance.entity) | Q(is_sticky_everywhere = True),importance__gte = 1).count()
            # add the good ones to the top items list
            top_items.extend(possible_top_items.filter(
                Q(hosted_by=instance.entity) | Q(is_sticky_everywhere = True),
                importance__gte = 1)
                )
            # if this date set contains any unimportant items, then there are no more to promote
            demotable_items = possible_top_items.exclude(
                Q(hosted_by=instance.entity) | Q(is_sticky_everywhere = True),
                importance__gte = 1
                )
            if demotable_items.count() > 0:
                # put those unimportant items into ordinary items
                ordinary_items.extend(demotable_items)
                # print "        demoting",  demotable_items.count()
                # and stop looking for any more
                break
        # and add everything left in non-sticky items before this date
        if dates:
            remaining_items = non_sticky_items.filter(date__lte=date)
            # print "    demoting the remaining", remaining_items.count()
            ordinary_items.extend(remaining_items)
            for item in top_items:
                item.sticky = True
                if instance.format == "title":
                    item.importance = None
            # print "Top items", len(top_items)
            # print "Ordinary items", len(ordinary_items)
            ordinary_items.sort(key=operator.attrgetter('date'), reverse = True)
        return top_items, ordinary_items




