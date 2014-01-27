from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from endpoint.http import JSONResponse
from endpoint.models import Pair
from endpoint.serializers import UserSerializer, GroupSerializer, PairSerializer


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PairViewSet(ModelViewSet):
    """
    API endpoint that allows key/value pairs to be created or retrieved.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Pair.objects.all()
    serializer_class = PairSerializer

    def get_queryset(self):
        """
        Only return pairs where the owner is the currently authenticated user.
        """
        model = self.serializer_class.Meta.model
        user = self.request.user
        return model.objects.filter(owner=user)

    def pre_save(self, obj):
        """
        Store the creator as owner with the object before saving.
        """
        obj.owner = self.request.user


class RegisterView(View):
    """
    API endpoint that allows a client to obtain a token by giving valid user credentials.
    """
    permission_classes = AllowAny

    @csrf_exempt
    def register(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
                return JSONResponse(token.key)
            return JSONResponse('Inactive user', status=401)
        return JSONResponse('User not found', status=401)