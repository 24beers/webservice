from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Pair.objects.all()
    serializer_class = PairSerializer

    def list(self, request):
        try:
            pairs = Pair.objects.get(owner=request.user.id)
        except Pair.DoesNotExist:
            return JSONResponse(None)
        serializer = PairSerializer(pairs, many=True)
        return JSONResponse(serializer.data)

    def pre_save(self, obj):
        obj.owner = self.request.user.username

    def retrieve(self, request, pk=None):
        data = JSONParser().parse(request)
        queryset = Pair.objects.get(data.token, key=pk)
        serializer = PairSerializer(queryset, many=True)
        return HttpResponse(serializer.data)


class RegisterView(View):
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
            return HttpResponse('Inactive user', status=401)
        return HttpResponse('User not found', status=401)


#class JSONResponse(HttpResponse):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)

#    def __init__(self, data, **kwargs):
#        content = JSONRenderer().render(data)
#        kwargs['content_type'] = 'application/json'
#        super(JSONResponse, self).__init__(content, **kwargs)

#    def create(self, request):
#        if request.method == 'PUT':
#            data = JSONParser().parse(request)
#            serializer = PairSerializer(data)
#            if serializer.is_valid():
#                serializer.save()
#                return JSONResponse(serializer.data)
#            return JSONResponse(serializer.errors, 400)
#        return JSONResponse(status=405)

#    def get(self, request):
#        if request.method == 'GET':
#            data = JSONParser().parse(request)
#            try:
#                if data.key != '':
#                    pair = Pair.objects.get(token=data.token, key=data.key)
#                else:
#                    pair = Pair.objects.get(token=data.token)
#            except Pair.DoesNotExist:
#                return HttpResponse(status=404)
#            serializer = PairSerializer(pair)
#            return JSONResponse(serializer.data)
#        return JSONResponse(status=405)