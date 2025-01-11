from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework import generics
from .models import BOM, ProductionOrder, Task, Product, Material, ProductRestock, MaterialRestock
from .serializers import *
from django.views import View
import json
from django.shortcuts import get_object_or_404


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
        
class CreateProductionOrderAPIView(APIView):

    def post(self, request):
        try:
            
            data = request.data
            order_ID = data.get('order_ID')
            order_date = data.get('order_date')
            product_name = data.get('product_name')
            product_quantity = data.get('product_quantity')
            material_name = data.get('material_name')
            order_deadline = data.get('order_deadline')

            print(f"收到的 order_date: {order_date}")
            print(f"收到的 product_name: {product_name}")
            print(f"收到的 product_quantity: {product_quantity}")
            print(f"收到的 material_name: {material_name}")
            print(f"收到的 order_deadline: {order_deadline}")

            if not all([order_ID, order_date, product_name, product_quantity, material_name, order_deadline]):
                return JsonResponse({'success': False, 'error': '所有欄位均為必填！'}, status=400)

            # 確保關聯的實例
            product_name = get_object_or_404(Product, product_name=product_name)
            material_name = get_object_or_404(Material, material_name=material_name)

            #計算物料數量
            if product_name.__eq__("排球上衣"):
                material_quantity = int(product_quantity) * 217
            elif product_name.__eq__("排球褲"):
                material_quantity = int(product_quantity) * 96
            elif product_name.__eq__("運動厚底短襪（1雙）"):
                material_quantity = int(product_quantity) * 30
            else:
                return JsonResponse({'success': False, 'error': '未知的產品名稱！'}, status=400)

            # 創建生產訂單
            ProductionOrder.objects.create(
                order_ID=order_ID,
                order_date=order_date,
                product_name=product_name,
                product_quantity=product_quantity,
                material_name=material_name,
                material_quantity=material_quantity,
                order_status="處理中",
                order_deadline=order_deadline
            )

            return JsonResponse({'success': True}, status=201)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

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
        instance.order_status = status
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

@method_decorator(csrf_exempt, name='dispatch')    
class CreateProductionTasksAPIView(APIView):

     def post(self, request):
        try:
            data = request.data
            order_ID = data.get('order_ID')  # 接收來自前端的主鍵值
            task_date = data.get('task_date')
            task_action = data.get('task_action')
            task_content = data.get('task_content')

            if not all([order_ID, task_date, task_action, task_content]):
                return JsonResponse({'success': False, 'error': '所有欄位均為必填！'}, status=400)

            # 確保 order_ID 是 ProductionOrder 的實例
            production_order = get_object_or_404(ProductionOrder, id=order_ID)

            # 創建代辦事項
            Task.objects.create(
                order_ID=production_order,  # 這裡傳入的是實例
                task_date=task_date,
                task_action=task_action,
                task_content=task_content
            )

            return JsonResponse({'success': True}, status=201)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

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