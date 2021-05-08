from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
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

    # id of the object in pk which you want to update
    # put will replace the object with the new one.
    def put(self, request, pk=None):
        """"Handle updating an object"""
        return Response({'method':'PUT'})

    # patch update a particular key value which is provided.
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

    # queryset is to define model
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', )


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    """Change header using modHeader extension in chrome"""
    """Authorization = Token d225cb749e778faa50d2613acdee4696cbb8fd5c"""

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,) # so that we can map user to the user_profile field if it is authenticated.
    serializer_class = serializers.ProfileFeedItemSerializer
    # objects will be inside the Model
    queryset = models.ProfileFeedItem.objects.all()

    permission_classes = (
            permissions.UpdateOwnStatus,
            IsAuthenticated # user must be authenticated to perform any request that is not a read request so that will get rid of the issue of users trying to create new feed item when they are not authenticated
    )
    # as we were getting error page as we unchecked the authentication element from heading using mode header externsion. To handle that error IsAuthenticatedOrReadOnly.

    # handy feature of the django rest frmework that allows you to override the behaviour to create objects trough a modelviewset
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        # when a request gets made to our viewset we can pass it to our serializer and validate it and then serializer.save function which is called by default.
        # so if we need to customize the logic for creation we need to override the function perform_create
        # this method is called everytime HTTP POST method called
        serializer.save(user_profile=self.request.user)
        # when a new object created, perform_create function will be called and it passes in the serializer that we are using to create the object.
        # the serializer is a model serializer so it has a save function(which is used to save the contents of the serializer to an object in the database) that is assigned to it.
