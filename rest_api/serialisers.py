from rest_framework import serializers
from datetime import datetime, date

from .models import JournalEntries


class JournalEntriesSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JournalEntries
        fields = ('submitted', 'intended_date', 'earth', 'water', 'air', 'fire')
        # fields = '__all__'

    def update(self, instance, validated_data):
        instance.submitted = validated_data.get('submitted', instance.submitted)
        instance.intended_date = validated_data.get('intended_date', instance.intended_date)
        instance.earth = validated_data.get('earth', instance.earth)
        instance.water = validated_data.get('water', instance.water)
        instance.air = validated_data.get('air', instance.air)
        instance.fire = validated_data.get('fire', instance.fire)
        instance.save()
        return instance