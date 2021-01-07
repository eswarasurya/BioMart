from rest_framework import serializers
from shopping.models import Product



class ProductSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=40)
    price = serializers.FloatField()
    quantity = serializers.FloatField()
    origin = serializers.CharField(max_length=200)


class ProductPostSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=40)
    mrp = serializers.FloatField()
    discount = serializers.FloatField()
    price = serializers.FloatField()
    quantity = serializers.FloatField()
    origin = serializers.CharField(max_length=200)
    description = serializers.CharField()

    def create(self, validated_data):
        return Product(**validated_data)

    def update(self, instance, validated_data):
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.mrp = validated_data.get('mrp', instance.mrp)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance  


class OriginSerializer(serializers.Serializer):
    origin = serializers.CharField(max_length=200)
