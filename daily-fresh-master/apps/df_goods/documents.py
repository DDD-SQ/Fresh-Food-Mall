"""
Elasticsearch 文档映射定义模块

本模块定义了商品信息在 Elasticsearch 中的索引结构，
包括字段类型、分词器配置、索引设置等。

主要功能：
1. 定义商品索引结构
2. 配置中文分词器
3. 建立Django模型与ES文档的映射关系
"""

from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import GoodsInfo, TypeInfo

# 创建商品索引对象，索引名称为 'goods'
goods_index = Index('goods')
# 配置索引设置
goods_index.settings(
    number_of_shards=1,      # 分片数量：1个（单机部署，无需分片）
    number_of_replicas=0     # 副本数量：0个（单机部署，无需副本）
)


@registry.register_document
class GoodsDocument(Document):
    """
    商品文档映射类
    
    将 Django 的 GoodsInfo 模型映射到 Elasticsearch 文档，
    定义每个字段在 ES 中的存储和索引方式。
    
    Attributes:
        gtitle: 商品名称，支持全文检索
        gjianjie: 商品简介，支持全文检索
        gcontent: 商品详情，支持全文检索
        gprice: 商品价格，数值类型
        gpic: 商品图片路径
        gclick: 商品点击量
        gkucun: 商品库存
        gunit: 商品单位
        gtype: 商品分类信息（嵌套对象）
    """
    
    # 商品名称字段
    gtitle = fields.TextField(
        analyzer='ik_max_word',       # 索引分词器：最大化分词，用于建立索引
        search_analyzer='ik_smart',   # 搜索分词器：智能分词，用于搜索查询
        fields={
            'raw': fields.KeywordField(),  # 子字段：原始值，用于精确匹配和排序
        }
    )
    
    # 商品简介字段
    gjianjie = fields.TextField(
        analyzer='ik_max_word',       # 索引时使用最大化分词
        search_analyzer='ik_smart'    # 搜索时使用智能分词
    )
    
    # 商品详情字段（富文本内容）
    gcontent = fields.TextField(
        analyzer='ik_max_word',       # 索引时使用最大化分词
        search_analyzer='ik_smart'    # 搜索时使用智能分词
    )
    
    # 商品价格字段（浮点数）
    gprice = fields.FloatField()
    
    # 商品图片路径（关键字类型，不进行分词）
    gpic = fields.KeywordField()
    
    # 商品点击量（整数）
    gclick = fields.IntegerField()
    
    # 商品库存（整数）
    gkucun = fields.IntegerField()
    
    # 商品单位（关键字类型，不进行分词）
    gunit = fields.KeywordField()
    
    # 商品分类信息（嵌套对象）
    gtype = fields.ObjectField(properties={
        'id': fields.IntegerField(),                      # 分类ID
        'ttitle': fields.TextField(analyzer='ik_smart'),  # 分类名称，支持中文分词
    })

    # 索引配置
    class Index:
        name = 'goods'  # 索引名称
        settings = {
            'number_of_shards': 1,      # 分片数
            'number_of_replicas': 0,    # 副本数
        }

    # Django模型关联配置
    class Django:
        model = GoodsInfo              # 关联的Django模型
        fields = [                     # 自动映射的字段
            'id',                      # 商品ID
            'isDelete',                # 逻辑删除标识
        ]
        related_models = [TypeInfo]    # 关联模型，用于更新关联数据

    def get_instances_from_related(self, related_instance):
        """
        从关联模型获取商品实例
        
        当分类信息更新时，自动更新该分类下的所有商品索引。
        
        Args:
            related_instance: 关联模型实例（TypeInfo）
            
        Returns:
            QuerySet: 该分类下的所有商品
        """
        if isinstance(related_instance, TypeInfo):
            return related_instance.goodsinfo_set.all()

    def prepare_gpic(self, instance):
        """
        准备图片字段数据
        
        将 ImageFieldFile 转换为字符串路径，以便序列化为 JSON。
        
        Args:
            instance: GoodsInfo 模型实例
            
        Returns:
            str: 图片路径字符串，如果无图片则返回空字符串
        """
        if instance.gpic:
            return str(instance.gpic)
        return ''

    def prepare_gprice(self, instance):
        """
        准备价格字段数据
        
        将 Decimal 类型转换为 float，以便序列化为 JSON。
        
        Args:
            instance: GoodsInfo 模型实例
            
        Returns:
            float: 价格浮点数
        """
        return float(instance.gprice) if instance.gprice else 0.0

    def prepare_gtype(self, instance):
        """
        准备分类字段数据
        
        构建分类信息的嵌套对象。
        
        Args:
            instance: GoodsInfo 模型实例
            
        Returns:
            dict: 分类信息字典
        """
        if instance.gtype:
            return {
                'id': instance.gtype.id,
                'ttitle': instance.gtype.ttitle,
            }
        return None
