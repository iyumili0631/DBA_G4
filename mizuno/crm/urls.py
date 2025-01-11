from django.urls import path
from . import views

urlpatterns = [
    # HTML 模板視圖 (跳轉頁面)
    path('customer_list/', views.customer_list, name='customer_list'),
    path('customer_order_list/', views.customer_order_list, name='customer_order_list'),
    path('sales_task_list/', views.sales_task_list, name='sales_task_list'),
    path('rfm_analysis_list/', views.rfm_analysis_list, name='rfm_analysis_list'),
    path('marketing_metrics_list/', views.marketing_metrics_list, name='marketing_metrics_list'),

    # API 視圖 
    # 新增修改刪除查詢
    path('api/customers/', views.CustomerAPIView.as_view(), name='customer_api'),
    path('api/customers/create/', views.CreateCustomerAPIView.as_view(), name='create_customer_api'),
    path('api/customer_names/', views.CustomerNameAPIView.as_view(), name='customer_names_api'),
    
    path('api/customer_orders/', views.CustomerOrderAPIView.as_view(), name='customer_order_api'),
    path('api/customer_orders/<int:pk>/', views.CustomerOrderDetailAPIView.as_view(), name='customer_order_api_detail'),
    
    path('api/sales_tasks/', views.SalesTaskAPIView.as_view(), name='sales_task_api'),
    path('api/sales_tasks/<int:pk>/', views.SalesTaskDetailAPIView.as_view(), name='sales_task_api_detail'),
    
    path('api/rfm_analysis/', views.RFMAnalysisAPIView.as_view(), name='rfm_analysis_api'),
    path('api/rfm_analysis/<int:pk>/', views.RFMAnalysisDetailAPIView.as_view(), name='rfm_analysis_api_detail'),
    
    path('api/marketing_metrics/', views.MarketingMetricsAPIView.as_view(), name='marketing_metrics_api'),
    path('api/marketing_metrics/<int:pk>/', views.MarketingMetricsDetailAPIView.as_view(), name='marketing_metrics_api_detail'),

    # 計算顧客指標 API(e.g.CLV)
     path('api/customers/<int:customer_ID>/update_metrics/', views.UpdateCustomerMetricsAPIView.as_view(), name='update_customer_metrics'),
    # 銷售趨勢 API
     path('marketing_trends/', views.marketing_trends_view, name='marketing_trends'),
    # 行銷數據更新 API
    path('api/marketing_metrics/update/', views.UpdateMarketingMetricsAPIView.as_view(), name='update_marketing_metrics'),
    # RFM分析 API
    path('api/rfm-analysis/calculate/', views.RFMAnalysisCalculateAPIView.as_view(), name='rfm_analysis_calculate'),
    #RFM觸發 API
    path('trigger_rfm_analysis/', views.trigger_rfm_analysis, name='trigger_rfm_analysis'),
]
