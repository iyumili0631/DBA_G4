from django.urls import path
from . import views

urlpatterns = [
    # HTML 模板視圖 (跳轉頁面)
    path('bom_list/', views.bom_list, name='bom_list'),
    path('production_order_list/', views.production_order_list, name='production_order_list'),
    path('production_task_list/', views.production_task_list, name='production_task_list'),
    path('product_list/', views.product_list, name='product_list'),
    path('material_list/', views.material_list, name='material_list'),
    path('product_restock_list/', views.product_restock_list, name='product_restock_list'),
    path('material_restock_list/', views.material_restock_list, name='material_restock_list'),

    # API 視圖 （新增修改刪除查詢）
    path('api/boms/', views.BOMAPIView.as_view(), name='bom_api'),
    path('api/boms/<int:pk>/', views.BOMDetailAPIView.as_view(), name='bom_api_detail'),
    path('api/production_orders/', views.ProductionOrderAPIView.as_view(), name='production_order_api'),
    path('api/production_orders/<int:pk>/', views.ProductionOrderDetailAPIView.as_view(), name='production_order_api_detail'),
    path('api/production_tasks/', views.TasksAPIView.as_view(), name='task_api'),
    path('api/production_tasks/<int:pk>/', views.TasksDetailAPIView.as_view(), name='task_api_detail'),
    path('api/products/', views.ProductsAPIView.as_view(), name='product_api'),
    path('api/products/<int:pk>/', views.ProductsDetailAPIView.as_view(), name='product_api_detail'),
    path('api/materials/', views.MaterialsAPIView.as_view(), name='material_api'),
    path('api/materials/<int:pk>/', views.MaterialsDetailAPIView.as_view(), name='material_api_detail'),
    path('api/product_restock/', views.ProductRestockAPIView.as_view(), name='product_restock_api'),
    path('api/product_restock/<int:pk>/', views.ProductRestockDetailAPIView.as_view(), name='product_restock_api_detail'),
    path('api/material_restock/', views.MaterialRestockAPIView.as_view(), name='material_restock_api'),
    path('api/material_restock/<int:pk>/', views.MaterialRestockDetailAPIView.as_view(), name='material_restock_api_detail'),
]
