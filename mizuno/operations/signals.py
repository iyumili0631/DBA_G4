from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import *
from crm.models import *

# 新增生產訂單時產品庫存增加，物料庫存減少
@receiver(post_save, sender=ProductionOrder)
def update_inventory_on_production_order(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            # 獲取生產訂單中的產品和物料
            product = instance.product_name
            material = instance.material_name
            product_quantity = int(instance.product_quantity)
            material_quantity = float(instance.material_quantity)

            # 更新產品庫存數量
            product.product_inventory += product_quantity

            # 更新產品庫存狀態
            if product.product_inventory <= product.product_safe_inventory:
                product.product_inventory_status = '低於安全庫存'
            elif product.product_inventory == 0:
                product.product_inventory_status = '缺貨'
            else:
                product.product_inventory_status = '充足'
            product.save()

            # 更新物料庫存數量
            material.material_inventory -= material_quantity

            # 更新物料庫存狀態
            if material.material_inventory <= material.material_safe_inventory:
                material.material_inventory_status = '低於安全庫存'
            elif material.material_inventory == 0:
                material.material_inventory_status = '缺貨'
            else:
                material.material_inventory_status = '充足'
            material.save()


# 顧客訂單時減少產品庫存
@receiver(post_save, sender=CustomerOrder)
def update_product_inventory_on_order(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            product = instance.order_product  # 订单中的产品
            order_quantity = instance.order_quantity  # 订购数量

            # 判断库存是否充足
            if product.product_inventory >= order_quantity:
                # 扣减库存
                product.product_inventory -= order_quantity
                product.save()

                # 更新产品库存状态
                if product.product_inventory <= product.product_safe_inventory:
                    product.product_inventory_status = '低於安全庫存'
                elif product.product_inventory == 0:
                    product.product_inventory_status = '缺貨'
                else:
                    product.product_inventory_status = '充足'

                product.save()
            else:
                raise ValueError(f"庫存不足，無法完成訂單，當前庫存為 {product.product_inventory}")
            


