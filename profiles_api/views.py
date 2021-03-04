from rest_framework.views import APIView
from rest_framework.response import Response


class HelloAPIView(APIView):
    """"Test API View"""

    def get(self, request, format=None):
        """Returns a list of APIView Features"""
        an_apiview = [
            'User HTTP methods and function (get, post, put, patch, delete).',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic.',
            'Is mapped manually to URLS',
        ]

        return Response({'message': 'Hello!', 'an_apiview':an_apiview})
