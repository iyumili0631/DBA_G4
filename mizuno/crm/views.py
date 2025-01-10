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
        serializer = CreateCustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 保存數據到數據庫
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 計算顧客指標 API
class UpdateCustomerMetricsAPIView(APIView):
    def post(self, request, customer_ID):
        try:
            customer = Customer.objects.get(customer_ID=customer_ID)
            customer.update_purchase_metrics()
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

# Sales Tasks API
class SalesTaskAPIView(generics.ListCreateAPIView):
    queryset = SalesTask.objects.all()
    serializer_class = SalesTaskSerializer

class SalesTaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalesTask.objects.all()
    serializer_class = SalesTaskSerializer

# RFM Analysis API
class RFMAnalysisAPIView(generics.ListCreateAPIView):
    queryset = RFMAnalysis.objects.all()
    serializer_class = RFMAnalysisSerializer

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