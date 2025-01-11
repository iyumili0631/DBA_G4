from rest_framework import serializers
from .models import *

class BOMSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_name.product_name')
    material_name = serializers.CharField(source='material_name.material_name')
    
    class Meta:
        model = BOM
        fields = '__all__'

class ProductionOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_name.product_name')
    material_name = serializers.CharField(source='material_name.material_name')

    class Meta:
        model = ProductionOrder
        fields = '__all__'

class ProductionOrderIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder
        fields = ['order_ID']

class CreateProductionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder
        fields = ['id', 'order_date', 'product_name', 'product_quantity', 'material_name', "material_quantity", 'order_status', 'order_deadline']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class MaterialNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['material_name']

class ProductRestockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRestock
        fields = '__all__'

class MaterialRestockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialRestock
        fields = '__all__'
