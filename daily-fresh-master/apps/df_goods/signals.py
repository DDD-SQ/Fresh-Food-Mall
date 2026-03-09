"""
Elasticsearch 索引信号处理模块

本模块通过 Django 信号机制实现商品数据与 Elasticsearch 索引的自动同步。
当商品信息发生变化（新增、修改、删除）时，自动更新对应的 ES 索引。

主要功能：
1. 商品保存时自动更新 ES 索引
2. 商品删除时自动删除 ES 索引文档
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import GoodsInfo
from .documents import GoodsDocument


@receiver(post_save, sender=GoodsInfo)
def update_goods_index(sender, instance, **kwargs):
    """
    商品保存信号处理函数
    
    当商品信息被创建或更新时，自动同步到 Elasticsearch 索引。
    
    触发时机：
    - 新增商品时
    - 修改商品信息时
    
    Args:
        sender: 发送信号的模型类（GoodsInfo）
        instance: 被保存的商品实例
        **kwargs: 额外参数（如created字段表示是否新建）
    """
    try:
        GoodsDocument().update(instance)
    except Exception as e:
        # ES 同步失败不影响主业务流程，仅打印警告
        import warnings
        warnings.warn(f'ES 索引同步失败 [{instance.gtitle}]: {e}')


@receiver(post_delete, sender=GoodsInfo)
def delete_goods_index(sender, instance, **kwargs):
    """
    商品删除信号处理函数
    
    当商品被删除时，自动从 Elasticsearch 索引中删除对应文档。
    
    触发时机：
    - 调用商品对象的 delete() 方法时
    - 调用 QuerySet 的 delete() 方法时（仅对单个对象）
    
    Args:
        sender: 发送信号的模型类（GoodsInfo）
        instance: 被删除的商品实例
        **kwargs: 额外参数
        
    Note:
        使用 try-except 捕获异常，防止索引中不存在该文档时报错
    """
    try:
        doc = GoodsDocument()
        doc.get(id=instance.id).delete()  # 根据ID获取文档并删除
    except Exception as e:
        # 文档不存在或删除失败时忽略异常
        import warnings
        warnings.warn(f'ES 索引删除失败 [{instance.gtitle}]: {e}')
