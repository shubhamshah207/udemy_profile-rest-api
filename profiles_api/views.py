from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

from profiles_api import serializers
from rest_framework import viewsets
from profiles_api import models
from profiles_api import permissions

class HelloAPIView(APIView):
    """"Test API View"""
    serializer_class = serializers.HelloSerializer
    def get(self, request, format=None):
        """Returns a list of APIView Features"""
        an_apiview = [
            'User HTTP methods and function (get, post, put, patch, delete).',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic.',
            'Is mapped manually to URLS',
        ]

        return Response({'message': 'Hello!', 'an_apiview':an_apiview})


    def post(self, request):
        """"Create a Hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk=None):
        """"Handle updating an object"""
        return Response({'method':'PUT'})


    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method':'PATCH'})


    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloSerializer
    """Test API ViewSet"""
    def list(self, request):
        """Return a hello message"""
        a_viewset = [
        'Uses actions (list, create, update, partial update)',
        'Automatically maps to url using Routers',
        'Provides more functionalities with less code'
        ]
        return Response({'message':'Hello!', 'a_viewset':a_viewset})


    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        #http://127.0.0.1:8000/api/hello-viewset/1/
        """Handle getting an object by its ID"""
        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method':'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle updating and creating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', )
