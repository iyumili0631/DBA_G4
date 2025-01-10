from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import generics
from .models import BOM, ProductionOrder, Task, Product, Material, ProductRestock, MaterialRestock
from .serializers import *

# ==========================
# HTML 模板視圖
# ==========================
# BOM
def bom_list(request):
    boms = BOM.objects.all()
    return render(request, 'operations/bom_list.html', {'boms': boms})

# Production Orders
def production_order_list(request):
    p_orders = ProductionOrder.objects.all()
    return render(request, 'operations/production_order_list.html', {'orders': p_orders})

# Tasks
def production_task_list(request):
    p_tasks = Task.objects.all()
    return render(request, 'operations/production_task_list.html', {'tasks': p_tasks})

# Products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'operations/product_list.html', {'products': products})

# Materials
def material_list(request):
    materials = Material.objects.all()
    return render(request, 'operations/material_list.html', {'materials': materials})

# Product Restock
def product_restock_list(request):
    p_restock = ProductRestock.objects.all()
    return render(request, 'operations/product_restock_list.html', {'p_restock': p_restock})

# Material Restock
def material_restock_list(request):
    m_restock = MaterialRestock.objects.all()
    return render(request, 'operations/material_restock_list.html', {'m_restock': m_restock})


# ==========================
# API 視圖 (JSON 回傳)
# ==========================
# BOM API
class BOMAPIView(APIView):
    def get(self, request, *args, **kwargs):
        boms = BOM.objects.all()
        serializer = BOMSerializer(boms, many=True)
        return Response(serializer.data)

class BOMDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BOM.objects.all()
    serializer_class = BOMSerializer

# Production Orders API
class ProductionOrderAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            orders = ProductionOrder.objects.all()
            serializer = ProductionOrderSerializer(orders, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class ProductionOrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # 驗證數據是否合法
        status = data.get("order_status", instance.order_status)

        if status not in ["處理中", "已完成", "已取消"]:
            return Response({"error": "Invalid status"}, status=400)

        # 更新數據
        instance.order_status = order_status
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)
    
class ProductionOrderIDAPIView(APIView):
    def get(self, request):
        IDs = ProductionOrder.objects.all()
        serializer = ProductionOrderIDSerializer(IDs, many=True)
        return Response(serializer.data)
    
# Tasks API
class TasksAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TasksDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # 驗證數據是否合法
        task_action = data.get("task_action", instance.task_action)
        task_status = data.get("task_status", instance.task_status)

        if task_action not in ["生產", "發貨", "訂購"]:
            return Response({"error": "Invalid task_action"}, status=400)
        if task_status not in ["未完成", "完成"]:
            return Response({"error": "Invalid task_status"}, status=400)

        # 更新數據
        instance.task_action = task_action
        instance.task_status = task_status
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)


# Products API
class ProductsAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductNameAPIView(APIView):
    def get(self, request):
        names = Product.objects.all()
        serializer = ProductNameSerializer(names, many=True)
        return Response(serializer.data)

# Materials API
class MaterialsAPIView(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class MaterialsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class MaterialNameAPIView(APIView):
    def get(self, request):
        names = Material.objects.all()
        serializer = MaterialNameSerializer(names, many=True)
        return Response(serializer.data)

# Product Restock API
class ProductRestockAPIView(generics.ListCreateAPIView):
    queryset = ProductRestock.objects.all()
    serializer_class = ProductRestockSerializer

class ProductRestockDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductRestock.objects.all()
    serializer_class = ProductRestockSerializer

# Material Restock API
class MaterialRestockAPIView(generics.ListCreateAPIView):
    queryset = MaterialRestock.objects.all()
    serializer_class = MaterialRestockSerializer

class MaterialRestockDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MaterialRestock.objects.all()
    serializer_class = MaterialRestockSerializer