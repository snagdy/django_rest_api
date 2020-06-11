import json

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from datetime import datetime, date
from pytz import timezone

from rest_api.models import JournalEntries
from rest_api.serialisers import JournalEntriesSerialiser


class JournalEntriesModelTest(APITestCase):

    def setUp(self):
        self.test_time = str(datetime.now(timezone('UTC')))
        self.test_date = str(date.today())
        kwargs_dict = {
            "submitted": self.test_time,
            "intended_date": self.test_date,
            "earth": 5,
            "water": 5,
            "air": 5,
            "fire": 5
        }
        self.an_entry = JournalEntries.objects.create(**kwargs_dict)

    def test_entry(self):
        """
        Tests that the data model objects initialise properly in the DB
        :return:
        """
        self.assertEqual(self.an_entry.submitted, self.test_time)
        self.assertEqual(self.an_entry.intended_date, self.test_date)
        self.assertEqual(self.an_entry.earth, 5)
        self.assertEqual(self.an_entry.water, 5)
        self.assertEqual(self.an_entry.air, 5)
        self.assertEqual(self.an_entry.fire, 5)


class BaseViewTest(APITestCase):

    client = APIClient

    @staticmethod  # we want this method to exist for the class, not instances
    def create_entry(submitted="", intended_date="", earth="", water="", air="", fire=""):

        params_dict = {
            'submitted': submitted,
            'intended_date': intended_date,
            'earth': earth,
            'water': water,
            'air': air,
            'fire': fire
        }

        # we capture the variables via context and use them to create a new object from the context dict
        if all(val != "" for val in params_dict):
            JournalEntries.objects.create(**params_dict)

    def make_request(self, kind='post', **kwargs):
        """
        Make a POST request to create an entry
        :param kind: HTTP verb
        :param kwargs: JSON arguments
        :return:
        """
        content_type = 'application/json'
        data = json.dumps(kwargs['data'])
        if kind == 'post':
            kwargs_dict = {'version': kwargs['version']}
            reverse_url = reverse('journal-entries-list-create', kwargs=kwargs_dict)
            return self.client.post(path=reverse_url, data=data, content_type=content_type)

        elif kind == 'put':
            kwargs_dict = {'version': kwargs['version'], 'pk': kwargs['id']}
            reverse_url = reverse('journal-entries-detail', kwargs=kwargs_dict)
            return self.client.put(path=reverse_url, data=data, content_type=content_type)

        else:
            return None

    def fetch_an_entry(self, pk=0):
        """
        Fetches an entry from the DB table whose primary key corresponds to the pk input param
        :param pk: Database table primary key
        :return:
        """
        kwargs_dict = {'version': 'v1', 'pk': pk}
        reverse_url = reverse('journal-entries-detail', kwargs=kwargs_dict)
        return self.client.get(reverse_url)

    def delete_an_entry(self, pk=0):
        kwargs_dict = {'version': 'v1', 'pk': pk}
        reverse_url = reverse('journal-entries-detail', kwargs=kwargs_dict)
        return self.client.delete(reverse_url)

    def setUp(self):
        # create a admin user
        self.user = User.objects.create_superuser(
            username='test_user',
            email='test@mail.com',
            password='testing',
            first_name='test',
            last_name='user',
        )
        # add test data to the test database
        self.create_entry(str(datetime.now(timezone('UTC'))), str(date.today()), '5', '5', '5', '5')
        self.create_entry(str(datetime.now(timezone('UTC'))), str(date.today()), '4', '4', '4', '4')
        self.create_entry(str(datetime.now(timezone('UTC'))), str(date.today()), '3', '3', '3', '3')
        # valid data test, must be strings as it passes through deserialiser for REST API
        self.valid_data = {
            "submitted": str(datetime.now(timezone('UTC'))),
            "intended_date": str(date.today()),
            "earth": 5,
            "water": 5,
            "air": 5,
            "fire": 5
        }
        self.valid_entry_id = 1
        # invalid data test with blank fields
        self.invalid_data = {
            "submitted": '',
            "intended_date": '',
            "earth": '',
            "water": '',
            "air": '',
            "fire": ''
        }
        self.invalid_entry_id = 100


class GetAllEntriesTest(BaseViewTest):

    def test_get_all_entries(self):
        """
        This test ensures that all entries added in our setup method exist when we make GET requests to the endpoint
        :return:
        """
        kwargs_dict = {'version': 'v1'}
        reverse_url = reverse('journal-entries-list-create', kwargs=kwargs_dict)
        response = self.client.get(reverse_url)
        expected = JournalEntries.objects.all()
        serialised = JournalEntriesSerialiser(expected, many=True)
        # check our response data matches our serialised expected data
        self.assertEqual(response.data, serialised.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleEntryTest(BaseViewTest):

    def test_get_an_entry(self):
        """
        This test checks that we can obtain an entry with a given ID, and show 404 if it is not found
        :return:
        """
        # hit the API endpoint to test its response
        response = self.fetch_an_entry(self.valid_entry_id)
        # get the database data directly for expected response
        expected = JournalEntries.objects.get(pk=self.valid_entry_id)
        # serialise data from DB
        serialised_expected = JournalEntriesSerialiser(expected)
        # check the API response is as expected and check status code is 200
        self.assertEqual(response.data, serialised_expected.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test an invalid query
        invalid_response = self.fetch_an_entry(self.invalid_entry_id)
        self.assertEqual(invalid_response.data['message'], "Entry with id 100 does not exist.")
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)


class AddEntryTest(BaseViewTest):

    def test_create_an_entry(self):
        """
        This test checks that a new entry can be added
        :return:
        """
        # hit the API endpoint to test its response to a POST request
        kwargs_dict = {
            'kind': 'post',
            'version': 'v1',
            'data': self.valid_data
        }
        response = self.make_request(**kwargs_dict)
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test an invalid response
        invalid_kwargs_dict = {
            'kind': 'post',
            'version': 'v1',
            'data': self.invalid_data
        }
        invalid_response = self.make_request(**invalid_kwargs_dict)
        message = f"The following parameters were missing from your request: {', '.join(self.invalid_data.keys())}"
        # check that our invalid response produced the expected response via the validation decorators in the view
        self.assertEqual(invalid_response.data['message'], message)
        self.assertEqual(invalid_response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateEntryTest(BaseViewTest):

    def test_update_an_entry(self):
        """
        This test checks that we can update an entry. We will update the second entry in the DB with valid data
        and update the third entry with invalid data, and test our assertions about responses
        :return:
        """
        # hit the API endpoint for a response using valid data
        kwargs_dict = {
            'kind': 'put',
            'version': 'v1',
            'id': 2,
            'data': self.valid_data
        }
        response = self.make_request(**kwargs_dict)
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # hit the API endpoint for a response using invalid data
        invalid_kwargs_dict = {
            'kind': 'put',
            'version': 'v1',
            'id': 3,
            'data': self.invalid_data
        }
        invalid_response = self.make_request(**invalid_kwargs_dict)
        message = f"The following parameters were missing from your request: {', '.join(self.invalid_data.keys())}"
        self.assertEqual(invalid_response.data['message'], message)
        self.assertEqual(invalid_response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteEntryTest(BaseViewTest):

    def test_delete_an_entry(self):
        """
        This test checks that an entry for a given ID can be deleted from the DB
        :return:
        """
        # hit the API endpoint
        response = self.delete_an_entry(1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # hit the API endpoint with a nonexistent ID
        invalid_response = self.delete_an_entry(100)
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)
