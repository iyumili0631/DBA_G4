from rest_framework import serializers
from .models import *

class BOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOM
        fields = '__all__'

class ProductionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ProductRestockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRestock
        fields = '__all__'

class MaterialRestockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialRestock
        fields = '__all__'
