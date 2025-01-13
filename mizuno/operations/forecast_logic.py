from datetime import timedelta, date
from .models import Product, Material, ProductRestock, MaterialRestock
from django.db import transaction
from django.shortcuts import get_object_or_404

def calculate_product_forecast_and_restock():
    """
    計算產品的需求預測並創建補貨計劃
    """
    today = date.today()
    restock_date = today.replace(day=1)  # 每月1號補貨
    start_date = today - timedelta(days=90)  # 過去三個月
    end_date = today

    with transaction.atomic():
        for product in Product.objects.all():
            # 計算過去三個月的平均銷售量
            orders = product.customerorder_set.filter(order_date__range=(start_date, end_date))
            total_quantity = sum(order.order_quantity for order in orders)
            months = 3  # 固定為三個月
            avg_sales = total_quantity // months  # 平均銷量

            # 補貨數量計算
            restock_quantity = max(0, avg_sales - product.product_inventory)

            # 從 product 實例中獲取所需屬性
            product_name = product.product_name
            product_inventory = product.product_inventory
            product_safe_inventory = product.product_safe_inventory

            # 創建或更新補貨計劃
            ProductRestock.objects.update_or_create(
                product_name=product,  # 傳遞整個 product 物件
                restock_date=restock_date,
                product_prediction=avg_sales,
                product_inventory=product,
                product_safe_inventory=product,
                restock_quantity=restock_quantity,
            )

def calculate_material_forecast_and_restock():
    """
    計算物料的需求預測並創建補貨計劃
    """
    today = date.today()
    restock_date = today.replace(day=1)  # 每月1號補貨
    start_date = today - timedelta(days=90)  # 過去三個月
    end_date = today

    with transaction.atomic():
        for material in Material.objects.all():
            # 計算過去三個月內使用的物料總量
            production_orders = material.order_material_name.filter(order_date__range=(start_date, end_date))
            total_quantity_used = sum(order.material_quantity for order in production_orders)
            months = 3  # 固定為三個月
            avg_usage = total_quantity_used // months  # 平均用量

            # 補貨數量計算
            restock_quantity = max(0, avg_usage - material.material_inventory)

            # 從 material 實例中獲取所需屬性
            material_name = material.material_name
            material_inventory = material.material_inventory
            material_safe_inventory = material.material_safe_inventory

            # 創建或更新補貨計劃
            MaterialRestock.objects.update_or_create(
                material_name=material,  # 傳遞整個 material 物件
                restock_date=restock_date,
                material_prediction=avg_usage,
                material_inventory=material,
                material_safe_inventory=material,
                restock_quantity=restock_quantity,
            )
