from django.db import models

# Create your models here.

# 產品庫存
class Product(models.Model):
    product_ID = models.IntegerField(unique = True)
    product_name = models.CharField(max_length=255)
    product_price = models.IntegerField(null = True, blank = True)
    product_inventory = models.IntegerField()
    product_safe_inventory = models.IntegerField()
    product_inventory_status = models.CharField(max_length=50, choices=[('充足', '充足'), ('低於安全庫存', '低於安全庫存'), ('缺貨', '缺貨')])

    def __str__(self):
        return f"{self.product_name}"

# 物料庫存
class Material(models.Model):
    material_ID = models.IntegerField()
    material_name = models.CharField(max_length=255)
    material_inventory = models.IntegerField()
    material_safe_inventory = models.IntegerField()
    material_inventory_status = models.CharField(max_length=50, choices=[('充足', '充足'), ('低於安全庫存', '低於安全庫存'), ('缺貨', '缺貨')])

    def __str__(self):
        return f"{self.material_name}"
    
# BOM 表
class BOM(models.Model):
    BOM_ID = models.IntegerField()
    product_name = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='bom_product_name')
    material_name = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    material_quantity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.product_name}"

# 生產訂單
class ProductionOrder(models.Model):
    order_ID = models.IntegerField()
    order_date = models.DateField()
    product_name = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='order_product_name')
    product_quantity = models.IntegerField()
    material_name = models.ForeignKey(Material, on_delete=models.DO_NOTHING, related_name='order_material_name')
    material_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, choices=[('處理中', '處理中'), ('已完成', '已完成'), ('已取消', '已取消')])
    order_deadline = models.DateField()

    def __str__(self):
        return f"{self.order_ID}"

import re
from decimal import Decimal

def extract_text_and_numbers(input_text):
    """
    從輸入文本中提取中文字串和數字
    :param input_text: 包含文字和數字的字符串
    :return: tuple (中文字串, 數字列表)
    """
    # 提取中文字串
    chinese_text = ''.join(re.findall(r'[\u4e00-\u9fff]+', input_text))
    
    # 提取數字
    numbers = re.findall(r'\d+', input_text)
    numbers = [int(num) for num in numbers] # 將數字轉換為int列表
    
    return chinese_text, numbers

# 待辦事項
class Task(models.Model):
    order_ID = models.ForeignKey(ProductionOrder, on_delete=models.DO_NOTHING, related_name='task_order_id')
    task_date = models.DateField()
    task_action = models.CharField(max_length=50, choices=[('生產', '生產'), ('發貨', '發貨'), ('訂購', '訂購')])
    task_content = models.TextField()
    task_status = models.CharField(max_length=50, choices=[('未完成', '未完成'), ('完成', '完成')])

    def process_field(self):
        chinese, numbers = extract_text_and_numbers(self.task_content)
        return chinese, numbers


# 產品補貨機制
class ProductRestock(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='restock_product_name')
    product_prediction = models.IntegerField()
    product_inventory = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='restock_product_inventory')
    product_safe_inventory = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='restock_product_safe_inventory')
    restock_date = models.DateField()
    restock_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product_name}"


#物料補貨機制
class MaterialRestock(models.Model):
    material_name = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='restock_material_name')
    material_prediction = models.IntegerField()
    material_inventory = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='restock_material_inventory')
    material_safe_inventory = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='restock_material_safe_inventory')
    restock_date = models.DateField()
    restock_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.material_name}"
    




