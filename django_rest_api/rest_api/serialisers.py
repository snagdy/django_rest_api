from rest_framework import serializers
from .models import JournalEntries


class JournalEntriesSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JournalEntries
        fields = ('submitted', 'intended_date', 'earth', 'water', 'air', 'fire')