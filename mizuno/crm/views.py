from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.views import status
from .models import Customer, CustomerOrder, SalesTask, RFMAnalysis, MarketingMetrics
from .serializers import *
from django.apps import apps
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils.decorators import method_decorator

# ==========================
# HTML 模板視圖
# ==========================
# Customers
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'crm/customer_list.html', {'customers': customers})

# Customer Orders
def customer_order_list(request):
    orders = CustomerOrder.objects.all()
    return render(request, 'crm/customer_order_list.html', {'orders': orders})

# Sales Tasks
def sales_task_list(request):
    tasks = SalesTask.objects.all()
    return render(request, 'crm/sales_task_list.html', {'tasks': tasks})

# RFM Analysis
def rfm_analysis_list(request):
    analyses = RFMAnalysis.objects.all()
    return render(request, 'crm/rfm_analysis_list.html', {'rfm_analyses': analyses})

# Marketing Metrics
def marketing_metrics_list(request):
    metrics = MarketingMetrics.objects.all()
    return render(request, 'crm/marketing_metrics_list.html', {'metrics': metrics})

# 行銷趨勢圖
def marketing_trends_view(request):
    # 獲取所有的行銷數據，並按年份和季度排序
    metrics = MarketingMetrics.objects.all().order_by('year', 'quarter')

      # 提取數據到圖表
    labels = [f"{m.year} {m.quarter}" for m in metrics]
    sales_data = [m.quarter_sales for m in metrics]
    growth_rate_data = [m.quarter_growth_rate for m in metrics]

    # 將數據傳遞給模板
    return render(request, 'crm/marketing_trends.html', {
        'labels': list(labels),
        'sales_data': list(sales_data),
        'growth_rate_data': list(growth_rate_data),
    })


# ==========================
# API 視圖 (JSON 返回)
# ==========================
# Customer API
class CustomerAPIView(APIView):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

class CreateCustomerAPIView(APIView):

    def post(self, request):
        """
        接收 POST 請求來新增顧客
        """
        # 獲取請求中的資料
        # data = json.loads(request.data)
        data = request.data
        customer_ID = data.get('customer_ID')  # 從 JSON 中取出 customer_ID
        name = data.get('name')  # 從 JSON 中取出 name

        # 驗證是否有必要的資料
        if not customer_ID or not name:
            return Response(
                {'success': False, 'error': '缺少必要欄位！'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 將資料存入資料庫
        try:
            Customer.objects.create(customer_ID=customer_ID, name=name)
            return Response(
                {'success': True, 'message': '顧客新增成功！'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': f'新增顧客失敗：{str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomerNameAPIView(APIView):
    def get(self, request):
        names = Customer.objects.all()
        serializer = CustomerNameSerializer(names, many=True)
        return Response(serializer.data)

# 計算顧客指標 API
class UpdateCustomerMetricsAPIView(APIView):
    def post(self, request, customer_ID):
        try:
            customer = Customer.objects.get(customer_ID=customer_ID)
            customer.update_purchase_metrics()
            customer.calculate_clv()
            customer.save()

            return Response({
                "message": "Customer metrics updated successfully",
                "customer_ID": customer.customer_ID,
                "last_purchase_date": customer.last_purchase_date,
                "avg_purchase_interval": customer.avg_purchase_interval,
                "avg_purchase_value": customer.avg_purchase_value,
                "lifetime_value": customer.lifetime_value,
            }, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

# Customer Order API
class CustomerOrderAPIView(APIView):
    def get(self, request, *args, **kwargs):
        orders = CustomerOrder.objects.all()
        serializer = CustomerOrderSerializer(orders, many=True)
        return Response(serializer.data)

class CustomerOrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerOrder.objects.all()
    serializer_class = CustomerOrderSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # 驗證數據是否合法
        newStatus = data.get("status", instance.status)

        if newStatus not in ["已完成", "處理中", "已取消"]:
            return Response({"error": "Invalid task_action"}, status=400)
        
        # 更新數據
        instance.status = newStatus
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

class CreateCustomerOrdersAPIView(APIView):

    def post(self, request):
        try:
            
            data = request.data
            customer = data.get('customer')
            order_ID = data.get('order_ID')
            order_date = data.get('order_date')
            order_product = data.get('order_product')
            order_quantity = data.get('order_quantity')
            

            if not all([customer, order_ID, order_date, order_product, order_quantity]):
                return JsonResponse({'success': False, 'error': '所有欄位均為必填！'}, status=400)

            # 確保 order_ID 和 order_quantity 是數字
            try:
                order_ID = int(order_ID)
                order_quantity = int(order_quantity)
            except ValueError:
                return JsonResponse({'success': False, 'error': '訂單編號和訂購量必須為數字！'}, status=400)
            
            # 確保關聯的實例
            customer = get_object_or_404(Customer, name=customer)

            # 獲取 operations 中的 Product 模型
            Product = apps.get_model('operations', 'Product')

            # 根據 product_name 查找 Product 實例
            order_product = get_object_or_404(Product, product_name=order_product)

            # 將 order_date 轉換為 datetime 對象
            try:
                order_date = datetime.strptime(order_date, '%Y-%m-%d').date()  # 假設前端傳入的格式為 "YYYY-MM-DD"
            except ValueError:
                return JsonResponse({'success': False, 'error': '無效的日期格式，應為 YYYY-MM-DD'}, status=400)

            # 計算要求送達日期
            required_delivery_date = order_date + timedelta(days=5)

            # 創建顧客訂單
            CustomerOrder.objects.create(
                customer=customer,
                order_ID=order_ID,
                order_date=order_date,
                order_product=order_product,
                order_quantity=order_quantity,
                required_delivery_date=required_delivery_date,
                status="處理中",
                
            )

            return JsonResponse({'success': True}, status=201)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Sales Tasks API
class SalesTaskAPIView(generics.ListCreateAPIView):
    queryset = SalesTask.objects.all()
    serializer_class = SalesTaskSerializer

class SalesTaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalesTask.objects.all()
    serializer_class = SalesTaskSerializer

# RFM Analysis API
class RFMAnalysisAPIView(APIView):
    def get(self, request, *args, **kwargs):
        RFMs = RFMAnalysis.objects.all()
        serializer = RFMAnalysisSerializer(RFMs, many=True)
        return Response(serializer.data)

class RFMAnalysisDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RFMAnalysis.objects.all()
    serializer_class = RFMAnalysisSerializer

class RFMAnalysisCalculateAPIView(APIView):
    """
    手動觸發 RFM 分析的計算並更新數據庫。
    """
    def post(self, request, *args, **kwargs):
        try:
            # 创建 RFMAnalysis 的实例并调用 RFM 计算逻辑
            rfm_analysis_instance = RFMAnalysis()  # 实例化对象
            rfm_analysis_instance.calculate_rfm()  # 通过实例调用 calculate_rfm()

            # 返回所有最新的 RFM 分析數據
            rfm_analyses = RFMAnalysis.objects.all()
            serializer = RFMAnalysisSerializer(rfm_analyses, many=True)

            return Response({
                "message": "RFM analysis updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": f"Failed to calculate RFM analysis: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def trigger_rfm_analysis(request):
    RFMAnalysis.calculate_rfm()
    return JsonResponse({'status': 'success', 'message': 'RFM 分析計算成功！'})

# Marketing Metrics API
class MarketingMetricsAPIView(generics.ListCreateAPIView):
    """
    提供 MarketingMetrics 表的列表和創建功能
    """
    queryset = MarketingMetrics.objects.all()
    serializer_class = MarketingMetricsSerializer


class MarketingMetricsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    提供單一 MarketingMetrics 行的檢索、更新和刪除功能
    """
    queryset = MarketingMetrics.objects.all()
    serializer_class = MarketingMetricsSerializer

class UpdateMarketingMetricsAPIView(APIView):
    """
    手動更新 MarketingMetrics 表中的行銷數據
    """
    def post(self, request):
        try:
            # 查看接收到的數據
            print("Request data:", request.data)  # 查看後端接收到的數據

            # 確保從前端接收的數據包含 'sales_data' 和 'growth_data'
            sales_data = request.data.get('sales_data', {})
            growth_data = request.data.get('growth_data', {})

            # 查看解析後的數據
            print("Parsed sales_data:", sales_data)
            print("Parsed growth_data:", growth_data)

            # 確保數據不為空
            if not sales_data or not growth_data:
                return Response(
                    {"error": "Missing sales_data or growth_data"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 計算行銷數據
            sales_data = MarketingMetrics.calculate_marketing_trends()
            growth_data = MarketingMetrics.calculate_growth_rate(sales_data)

            # 儲存計算後的數據
            MarketingMetrics.save_marketing_metrics(sales_data, growth_data)

            return Response(
                {"message": "Marketing metrics updated successfully", 
                 "sales_data": sales_data, 
                 "growth_data": growth_data}, 
                status=status.HTTP_200_OK
            )

        except Exception as e:
            # 捕獲錯誤並返回詳細的錯誤信息
            return Response(
                {"error": str(e), "details": "An error occurred while updating marketing metrics."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
