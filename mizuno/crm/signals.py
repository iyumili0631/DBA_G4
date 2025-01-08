from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=CustomerOrder)
def update_marketing_metrics(sender, instance, **kwargs):
    # 計算並更新行銷數據
    sales_data = MarketingMetrics.calculate_marketing_trends()
    growth_data = MarketingMetrics.calculate_growth_rate(sales_data)
    #MarketingMetrics.save_marketing_metrics(sales_data, growth_data)



