from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import *
from crm.models import *

# 補貨時更新產品庫存
@receiver(post_save, sender=ProductRestock)
def update_product_inventory_on_restock(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            product = instance.product_name  # 关联的产品
            restock_quantity = instance.restock_quantity  # 補貨數量

            # 更新產品庫存
            product.product_inventory += restock_quantity
            product.save()

            # 更新產品庫存狀態
            if product.product_inventory <= product.product_safe_inventory:
                product.product_inventory_status = '低於安全庫存'
            elif product.product_inventory == 0:
                product.product_inventory_status = '缺貨'
            else:
                product.product_inventory_status = '充足'

            product.save()

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
