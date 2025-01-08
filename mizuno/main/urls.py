from django.urls import path
from . import views

urlpatterns = [
     # 主頁路徑，指向主頁視圖
    path('', views.main, name='main'),
    
    # 跳轉到 CRM 頁面
    path('CRM/', views.crm, name='CRM'),
    
    # 跳轉到 OM 頁面
    path('OM/', views.om, name='OM'),
]
