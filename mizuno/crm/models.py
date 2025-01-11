from django.db import models, transaction
from datetime import timedelta
from django.db.models import Sum
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils import timezone

# Create your models here.


# 顧客清單
class Customer(models.Model):
    customer_ID = models.IntegerField(unique = True) # 確保 customer_ID 唯一
    name = models.CharField(max_length=255)
    last_purchase_date = models.DateField(null = True, blank = True)
    avg_purchase_interval = models.IntegerField(default = 0, blank = True)  # 平均購買間隔（天）
    avg_purchase_value = models.FloatField(default = 0, blank = True) # 平均客單價（NTD）
    avg_customer_years = models.FloatField(default = 3, blank = True) #平均客戶關係維持年數（年） 預設為3年
    lifetime_value = models.FloatField(default = 0, blank = True) #CLV 預設為0
    
    # 標志位，避免遞歸調用
    #_is_saving = False

    def update_purchase_metrics(self):
            """
            更新該客戶的購買相關數據：
            - last_purchase_date
            - avg_purchase_interval
            - avg_purchase_value
            """
            # 獲取該客戶的所有訂單
            orders = self.customerorder_set.all().order_by('order_date')
            order_count = orders.count()

            if order_count == 0:
                # 如果沒有訂單，清空購買相關數據
                self.last_purchase_date = None
                self.avg_purchase_interval = 0
                self.avg_purchase_value = 0
                self.save()
                return

            # 更新 last_purchase_date
            self.last_purchase_date = orders.last().order_date

            # 計算 avg_purchase_interval
            if order_count > 1:
                intervals = [
                    (orders[i].order_date - orders[i - 1].order_date).days
                    for i in range(1, order_count)
                ]
                self.avg_purchase_interval = sum(intervals) / len(intervals)
            else:
                self.avg_purchase_interval = 0  # 只有一筆訂單時無法計算間隔

            # 計算 avg_purchase_value
            total_order_value = sum(order.order_quantity * order.order_product.product_price for order in orders)
            self.avg_purchase_value = total_order_value / order_count

    def calculate_clv(self):
        """
        計算並返回 CLV（顧客終身價值）   
        根据公式：CLV = (平均客單價 * 每年交易次數) * 平均客戶關係維持年數     
        """
        if self.avg_purchase_interval <= 0 or self.avg_customer_years <= 0:
            return 0
        
         # 计算每年交易次数
        transactions_per_year = 365 / self.avg_purchase_interval
        
        # 计算 CLV
        clv = self.avg_purchase_value * transactions_per_year * self.avg_customer_years
        return round(clv, 2)

    def save(self, *args, **kwargs):
        # 在保存時自動更新購買相關數據和 CLV
        if self.pk: # 避免遞歸調用
            self.update_purchase_metrics()
            self.lifetime_value = self.calculate_clv()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_ID} - {self.name}"
    
    def __repr__(self):
        return self.name

# 顧客訂單
class CustomerOrder(models.Model):
    customer = models.ForeignKey('crm.Customer', on_delete=models.DO_NOTHING)
    order_ID = models.IntegerField()
    order_date = models.DateField()
    order_product = models.ForeignKey('operations.Product', on_delete=models.DO_NOTHING) # 外鍵關聯到 Product
    order_quantity = models.IntegerField()
    required_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('處理中', '處理中'), ('已完成', '已完成'), ('已取消', '已取消')])

    def __str__(self):
        return f"Order {self.order_ID} for {self.customer.name} - {self.order_product.product_name}"

    def save(self, *args, **kwargs):
        # 如果使用者沒有手動設置 required_delivery_date，就設置為 order_date 的 5 天後
        if self.required_delivery_date is None and self.order_date:
            self.required_delivery_date = self.order_date + timedelta(days=5)
        super().save(*args, **kwargs)

# 待辦事項
class SalesTask(models.Model):
    order_ID = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    task_ID = models.IntegerField()
    task_date = models.DateField()
    task_action = models.CharField(max_length=50, choices=[('發貨', '發貨'), ('退貨', '退貨')])
    task_content = models.TextField()
    task_status = models.CharField(max_length=50, choices=[('未完成', '未完成'), ('完成', '完成')])

# RFM 分析模型
class RFMAnalysis(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    recency = models.IntegerField(default=0, blank=True)
    frequency = models.IntegerField(default=0, blank=True)
    monetary = models.FloatField(default=0, blank=True)
    rfm_value = models.FloatField(default=0, blank=True)
    customer_group = models.CharField(max_length=255, blank=True)
    most_valuable_customer = models.CharField(max_length=255, blank=True)
    marketing_strategy_suggestion = models.TextField(blank=True)

    @staticmethod
    def calculate_rfm():
        try:
            # 獲取所有顧客
            customers = Customer.objects.all()
            rfm_results = []

            for customer in customers:
                # 獲取該顧客的訂單
                orders = customer.customerorder_set.all()

                if orders.exists():  # 確保有訂單
                    last_order_date = orders.latest('order_date').order_date
                    recency = (now().date() - last_order_date).days
                    frequency = orders.count()
                    monetary = sum(order.order_quantity * order.order_product.product_price for order in orders)

                    # 打印出調試信息
                    print(f"Customer: {customer.name}, Orders: {orders.count()}, Recency: {recency}, Frequency: {frequency}, Monetary: {monetary}")

                    # 計算 RFM 分數
                    r_score = 3 if recency <= 30 else (2 if recency <= 90 else 1)
                    f_score = 3 if frequency >= 5 else (2 if frequency >= 3 else 1)
                    m_score = 3 if monetary >= 3000 else (2 if monetary >= 1500 else 1)

                    rfm_value = r_score + f_score + m_score

                    if rfm_value >= 8:
                        customer_group = '高價值顧客'
                    elif 5 <= rfm_value < 8:
                        customer_group = '中價值顧客'
                    else:
                        customer_group = '低價值顧客'

                    if customer_group == '高價值顧客':
                        suggestion = '優先滿足需求或提供專屬優惠及 VIP 服務，提升顧客忠誠度。'
                    elif customer_group == '中價值顧客':
                        suggestion = '推送促銷活動，鼓勵更多購買行為。'
                    else:
                        suggestion = '發送喚回優惠，吸引顧客再次購買。'

                    # 準備好 RFM 結果
                    rfm_results.append(
                        RFMAnalysis(
                            customer=customer,
                            recency=recency,
                            frequency=frequency,
                            monetary=monetary,
                            rfm_value=rfm_value,
                            customer_group=customer_group,
                            most_valuable_customer="O" if customer_group == '高價值顧客' else '',
                            marketing_strategy_suggestion=suggestion
                        )
                    )
                else:
                    print(f"Customer {customer.name} has no orders.")
            
            # 批量保存 RFM 分析結果
            with transaction.atomic():
                RFMAnalysis.objects.bulk_create(
                    rfm_results, 
                    update_conflicts=True, 
                    unique_fields=['customer'],
                    update_fields=[
                        'recency',
                        'frequency',
                        'monetary',
                        'rfm_value',
                        'customer_group',
                        'most_valuable_customer',
                        'marketing_strategy_suggestion',
                    ]
                )
            print("RFM analysis completed successfully.")
            return rfm_results

        except Exception as e:
            print(f"RFM 分析計算失敗: {e}")

    def save(self, *args, **kwargs):
        # 在保存時自動更新
        if self.pk: # 避免遞歸調用
            self.calculate_rfm()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.name}: {self.rfm_value}"


# 行銷指標
class MarketingMetrics(models.Model):
    year = models.IntegerField(null=True, blank=True)
    quarter = models.CharField(max_length=255, null=True, blank=True)
    quarter_sales = models.FloatField(null=True, blank=True)
    quarter_growth_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @staticmethod
    def get_quarter(month):
        """計算季度"""
        return (month - 1) // 3 + 1

    @staticmethod
    def initialize_year_structure(sales_data, year):
        """初始化年度結構"""
        if year not in sales_data:
            sales_data[year] = {1: 0, 2: 0, 3: 0, 4: 0}

    @staticmethod
    def calculate_marketing_trends():
        """計算每年每季度的銷售額"""
        # 獲取所有訂單
        orders = CustomerOrder.objects.all()

        # 存儲每年每季度的銷售數據
        sales_data = {}

        for order in orders:
            # 驗證訂單數據
            if not order.order_date or order.order_quantity <= 0:
                continue

            # 計算年份和季度
            year = order.order_date.year
            quarter = MarketingMetrics.get_quarter(order.order_date.month)

            # 確保產品價格有效
            if not order.order_product or order.order_product.product_price is None:
                continue

            # 計算銷售額
            order_sales = order.order_quantity * order.order_product.product_price

            # 初始化並累加銷售額
            MarketingMetrics.initialize_year_structure(sales_data, year)
            sales_data[year][quarter] += order_sales

        return sales_data

    @staticmethod
    def calculate_growth_rate(sales_data):
        """計算季度銷售成長率"""
        growth_data = {}

        for year, quarters in sales_data.items():
            growth_data[year] = {}
            for quarter in range(1, 5):
                current_sales = quarters[quarter]
                if quarter == 1:
                    growth_data[year][quarter] = None  # 無前季度數據
                else:
                    previous_sales = quarters[quarter - 1]
                    growth_data[year][quarter] = (
                        (current_sales - previous_sales) / previous_sales * 100
                        if previous_sales > 0
                        else 0.0  # 或 'N/A'
                    )

        return growth_data
    
    @staticmethod
    def save_marketing_metrics(sales_data, growth_data):
        try:
            for year, quarters in sales_data.items():
                for quarter, sales in quarters.items():
                    growth_rate = growth_data.get(year, {}).get(quarter, None)
                    MarketingMetrics.objects.update_or_create(
                        year=year,
                        quarter=f"Q{quarter}",
                        defaults={
                            'quarter_sales': sales,
                            'quarter_growth_rate': growth_rate,
                        }
                    )
        except Exception as e:
            print(f"Error saving metrics: {e}")
            raise e  # 確保將錯誤傳遞給視圖處理


        

