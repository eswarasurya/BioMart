from rest_framework import serializers
from locations.models import loc



class LocationSerializer(serializers.Serializer):
    # loc_id = serializers.CharField()
    bno = serializers.CharField(max_length=200)
    street = serializers.CharField(max_length=200)
    area = serializers.CharField(max_length=200)
    state = serializers.CharField(max_length=200)
    owner = serializers.SlugRelatedField(read_only= True, slug_field='username')


class LocationSerializerPost(serializers.Serializer):
    bno = serializers.CharField(max_length=200)
    street = serializers.CharField(max_length=200)
    area = serializers.CharField(max_length=200)
    state = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return loc(**validated_data)

    def update(self, instance, validated_data):
        instance.bno = validated_data.get('bno', instance.bno)
        instance.street = validated_data.get('street', instance.street)
        instance.area = validated_data.get('area', instance.area)
        instance.state = validated_data.get('state', instance.state)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance  

