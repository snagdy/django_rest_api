# django_rest_api

This is just a small demo RESTful API built using the Django REST Framework, with a fair amount copied from this 
excellent tutorial here: https://github.com/kasulani/drf_tutorial

The data model is different, as this REST API is supposed to process time-series data, and the backend used in my
development setup is MySQL running within a Linux VM, with sqlite3 used only for unit tests.

For this differentiation between test and "production" DB, see: django_rest_api/settings.py

Will eventually get around to making this work with Docker + NGINX or Apache.