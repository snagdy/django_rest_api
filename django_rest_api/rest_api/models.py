from django.db import models
from datetime import datetime, date

# Create your models here.
class JournalEntries(models.Model):
    # entry_id = models.IntegerField(null=False)
    submitted = models.DateTimeField(default=datetime.now)
    intended_date = models.DateField(default=date.today)
    earth = models.IntegerField(null=False)
    water = models.IntegerField(null=False)
    air = models.IntegerField(null=False)
    fire = models.IntegerField(null=False)

    def __str__(self):
        return f"JournalEntry(submitted: {self.submitted}, intended_date: {self.intended_date}, " \
               f"earth: {self.earth}, water: {self.water}, air: {self.air}, fire: {self.fire})"