"""
更新商品拼音字段的管理命令

用于修复已存在商品的拼音字段为空的问题。
当添加拼音字段后，旧数据不会自动生成拼音，需要手动触发save()方法。
"""

from django.core.management.base import BaseCommand
from df_goods.models import GoodsInfo, TypeInfo


class Command(BaseCommand):
    help = '更新商品和分类的拼音字段'
    
    def handle(self, *args, **options):
        self.stdout.write('开始更新商品拼音字段...')
        
        goods_count = 0
        for goods in GoodsInfo.objects.all():
            goods.save()
            goods_count += 1
        
        self.stdout.write(f'已更新 {goods_count} 条商品数据')
        
        type_count = 0
        for t in TypeInfo.objects.all():
            t.save()
            type_count += 1
        
        self.stdout.write(f'已更新 {type_count} 条分类数据')
        self.stdout.write(self.style.SUCCESS('拼音字段更新完成!'))
