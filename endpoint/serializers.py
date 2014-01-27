from django.contrib.auth.models import User, Group
from rest_framework import serializers
from endpoint.models import Pair


class UserSerializer(serializers.HyperlinkedModelSerializer):
    pairs = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'pairs')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PairSerializer(serializers.ModelSerializer):
    value = serializers.CharField(required=False)
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = Pair
        fields = ('key', 'value', 'owner')