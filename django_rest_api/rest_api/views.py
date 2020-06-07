# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .serialisers import JournalEntriesSerialiser
from .models import JournalEntries


class ListCreateJournalEntriesView(generics.ListCreateAPIView):
    """
    GET journalentries/
    POST journalentries/
    """
    # the below handles GET requests to the endpoint
    queryset = JournalEntries.objects.all().order_by('id')
    serializer_class = JournalEntriesSerialiser

    # we override the post method of this class to handle POST requests to the endpoint
    def post(self, request, *args, **kwargs):
        an_entry = JournalEntries.objects.create(
            submitted = request.data['submitted'],
            intended_date = request.data['intended_date'],
            earth = request.data['earth'],
            water = request.data['water'],
            air = request.data['air'],
            fire = request.data['fire'],
        )
        return Response(
            data = JournalEntriesSerialiser(an_entry).data,
            status = status.HTTP_201_CREATED
        )


class JournalEntriesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET journalentries/:id/
    POST journalentries/:id/
    DELETE journalentries/:id/
    """
    queryset = JournalEntries.objects.all()
    serializer_class = JournalEntriesSerialiser


    def get(self, request, *args, **kwargs):
        print(kwargs)
        try:
            an_entry = self.queryset.get(pk=kwargs['pk'])
            return Response(JournalEntriesSerialiser(an_entry).data)
        except JournalEntries.DoesNotExist:
            message = f"Entry with id {kwargs['pk']} does not exist."
            return Response(
                data={
                    "message": message
                },
                status=status.HTTP_404_NOT_FOUND
            )


    def put(self, request, *args, **kwargs):
        try:
            an_entry = self.queryset.get(pk=kwargs['pk'])
            serialiser = JournalEntriesSerialiser()
            updated_entry = serialiser.update(an_entry, request.data) # passes data to serialiser as dict and updates
            return Response(JournalEntriesSerialiser(updated_entry).data)
        except JournalEntries.DoesNotExist:
            message = f"Entry with id {kwargs['pk']} does not exist."
            return Response(
                data={
                    "message": message
                },
                status=status.HTTP_404_NOT_FOUND
            )


    def delete(self, request, *args, **kwargs):
        try:
            an_entry = self.queryset.get(pk=kwargs['pk'])
            an_entry.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except JournalEntries.DoesNotExist:
            message = f"Entry with id {kwargs['pk']} does not exist."
            return Response(
                data={
                    "message": message
                },
                status=status.HTTP_404_NOT_FOUND
            )