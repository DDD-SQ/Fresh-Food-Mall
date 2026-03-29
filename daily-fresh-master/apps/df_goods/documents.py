"""
Elasticsearch 文档映射定义模块

本模块定义了商品信息在 Elasticsearch 中的索引结构，
包括字段类型、分词器配置、索引设置等。

主要功能：
1. 定义商品索引结构
2. 配置中文分词器（IK分词器）
3. [新增] 支持拼音搜索、英文搜索、模糊搜索
4. [新增] 支持分类关联搜索
5. 建立Django模型与ES文档的映射关系
"""

from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import GoodsInfo, TypeInfo

# 创建商品索引对象，索引名称为 'goods'
goods_index = Index('goods')

# [修改] 索引设置，新增拼音分词器配置
goods_index.settings(
    number_of_shards=1,      # 分片数量：1个（单机部署，无需分片）
    number_of_replicas=0,    # 副本数量：0个（单机部署，无需副本）
    # [新增] 分词器配置
    analysis={
        'analyzer': {
            # IK智能分词器：用于中文搜索时的分词处理
            'ik_smart': {
                'type': 'custom',
                'tokenizer': 'ik_smart'
            },
            # IK最大化分词器：用于索引时的分词处理，尽可能多地分词
            'ik_max_word': {
                'type': 'custom',
                'tokenizer': 'ik_max_word'
            },
            # [新增] 拼音分词器：用于拼音全拼搜索
            'pinyin_analyzer': {
                'type': 'custom',
                'tokenizer': 'ik_smart',
                'filter': ['pinyin_filter']
            },
            # [新增] 拼音首字母分词器：用于拼音首字母搜索
            'pinyin_abbr_analyzer': {
                'type': 'custom',
                'tokenizer': 'ik_smart',
                'filter': ['pinyin_abbr_filter']
            }
        },
        # [新增] 分词过滤器配置
        'filter': {
            # 拼音过滤器：保留完整拼音
            'pinyin_filter': {
                'type': 'pinyin',
                'keep_full_pinyin': True,      # 保留完整拼音
                'keep_original': False,        # 不保留原文
                'limit_first_letter_length': 16,
                'lowercase': True              # 转小写
            },
            # 拼音首字母过滤器：只保留首字母
            'pinyin_abbr_filter': {
                'type': 'pinyin',
                'keep_first_letter': True,     # 保留首字母
                'keep_full_pinyin': False,     # 不保留完整拼音
                'keep_original': False,
                'limit_first_letter_length': 16,
                'lowercase': True
            }
        }
    }
)


@registry.register_document
class GoodsDocument(Document):
    """
    商品文档映射类
    
    将 Django 的 GoodsInfo 模型映射到 Elasticsearch 文档，
    定义每个字段在 ES 中的存储和索引方式。
    
    [新增] 支持的搜索功能：
    1. 中文分词搜索（IK分词器）
    2. 拼音全拼搜索（如：caomei -> 草莓）
    3. 拼音首字母搜索（如：cm -> 草莓）
    4. 英文名称搜索（如：strawberry -> 草莓）
    5. 分类关联搜索（如：水果 -> 该分类下所有商品）
    6. 模糊搜索（容错处理）
    """
    
    # [修改] 商品名称字段，新增拼音和关键词子字段
    gtitle = fields.TextField(
        analyzer='ik_max_word',        # 索引时使用最大化分词
        search_analyzer='ik_smart',    # 搜索时使用智能分词
        fields={
            'raw': fields.KeywordField(),                                    # 原始值，用于精确匹配
            'pinyin': fields.TextField(analyzer='pinyin_analyzer'),          # [新增] 拼音子字段
            'pinyin_abbr': fields.TextField(analyzer='pinyin_abbr_analyzer'), # [新增] 拼音首字母子字段
            'keyword': fields.TextField(analyzer='ik_max_word'),              # [新增] 关键词子字段，用于模糊匹配
        }
    )
    
    # [新增] 商品名称拼音字段，独立存储拼音便于精确匹配
    gtitle_pinyin = fields.TextField(
        analyzer='pinyin_analyzer',
    )
    
    # [新增] 商品名称拼音首字母字段
    gtitle_pinyin_abbr = fields.TextField(
        analyzer='pinyin_abbr_analyzer',
    )
    
    # [新增] 商品英文名称字段，用于英文搜索
    gtitle_en = fields.KeywordField()
    
    # [修改] 商品简介字段，新增拼音子字段
    gjianjie = fields.TextField(
        analyzer='ik_max_word',
        search_analyzer='ik_smart',
        fields={
            'pinyin': fields.TextField(analyzer='pinyin_analyzer'),  # [新增] 拼音子字段
        }
    )
    
    # [新增] 商品简介拼音字段
    gjianjie_pinyin = fields.TextField(
        analyzer='pinyin_analyzer',
    )
    
    # 商品详情字段（富文本内容）
    gcontent = fields.TextField(
        analyzer='ik_max_word',
        search_analyzer='ik_smart'
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
    
    # [修改] 商品分类信息（嵌套对象），新增拼音和英文字段
    gtype = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'ttitle': fields.TextField(
            analyzer='ik_max_word',
            search_analyzer='ik_smart',
            fields={
                'pinyin': fields.TextField(analyzer='pinyin_analyzer'),          # [新增] 分类拼音
                'pinyin_abbr': fields.TextField(analyzer='pinyin_abbr_analyzer'), # [新增] 分类拼音首字母
            }
        ),
        'ttitle_pinyin': fields.TextField(analyzer='pinyin_analyzer'),  # [新增] 分类拼音字段
        'ttitle_en': fields.KeywordField(),                               # [新增] 分类英文字段
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
        [修改] 准备分类字段数据
        
        构建分类信息的嵌套对象，包含拼音和英文字段。
        
        Args:
            instance: GoodsInfo 模型实例
            
        Returns:
            dict: 分类信息字典
        """
        if instance.gtype:
            return {
                'id': instance.gtype.id,
                'ttitle': instance.gtype.ttitle,
                'ttitle_pinyin': instance.gtype.ttitle_pinyin or '',  # [新增] 分类拼音
                'ttitle_en': instance.gtype.ttitle_en or '',           # [新增] 分类英文名
            }
        return None

    def prepare_gtitle_pinyin(self, instance):
        """
        [新增] 准备商品名称拼音字段数据
        
        Args:
            instance: GoodsInfo 模型实例
            
        Returns:
            str: 商品名称拼音
        """
        return instance.gtitle_pinyin or ''

    def prepare_gtitle_pinyin_abbr(self, instance):
        """
        [新增] 准备商品名称拼音首字母字段数据
        
        Args:
            instance: GoodsInfo 模型实例
            
        Returns:
            str: 商品名称拼音首字母
        """
        return instance.gtitle_pinyin_abbr or ''

    def prepare_gtitle_en(self, instance):
        """
        [新增] 准备商品英文名称字段数据
        
        Args:
            instance: GoodsInfo 模型实例
            
        Returns:
            str: 商品英文名称
        """
        return instance.gtitle_en or ''

    def prepare_gjianjie_pinyin(self, instance):
        """
        [新增] 准备商品简介拼音字段数据
        
        Args:
            instance: GoodsInfo 模型实例
            
        Returns:
            str: 商品简介拼音
        """
        return instance.gjianjie_pinyin or ''
