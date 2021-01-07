from rest_framework import serializers
from blogs.models import blog


class BlogSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField()
    writer = serializers.SlugRelatedField(read_only= True, slug_field='username')
    pub_date = serializers.DateTimeField()


class BlogSerializerPost(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField()


    def create(self, validated_data):
        return blog(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.writer = validated_data.get('writer', instance.writer)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.save()
        return instance  

