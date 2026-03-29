"""
商品数据模型模块

本模块定义了商品分类和商品信息的数据模型，
包含拼音字段和英文字段，支持多语言搜索。

新增功能：
1. 自动生成拼音字段（用于拼音搜索）
2. 自动生成拼音首字母字段（用于首字母搜索）
3. 英文名称字段（用于英文搜索）
"""

from datetime import datetime

from django.db import models
from tinymce.models import HTMLField
# [新增] 导入拼音处理库，用于将中文转换为拼音
from pypinyin import lazy_pinyin, Style


class TypeInfo(models.Model):
    """
    商品分类信息模型
    
    字段说明：
    - isDelete: 逻辑删除标识
    - ttitle: 分类名称（如：新鲜水果、海鲜水产）
    - ttitle_pinyin: [新增] 分类名称拼音（如：xinxianshuiguo）
    - ttitle_en: [新增] 分类英文名称（如：fruit）
    """
    isDelete = models.BooleanField(default=False)
    ttitle = models.CharField(max_length=20, verbose_name="分类")
    # [新增] 分类拼音字段，用于拼音搜索
    ttitle_pinyin = models.CharField(max_length=100, verbose_name="分类拼音", blank=True, default='')
    # [新增] 分类英文名称字段，用于英文搜索
    ttitle_en = models.CharField(max_length=100, verbose_name="分类英文名", blank=True, default='')

    class Meta:
        verbose_name = "商品类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ttitle

    def save(self, *args, **kwargs):
        """
        [新增] 重写保存方法，自动生成拼音字段
        
        当保存分类时，如果拼音字段为空，则自动根据中文名称生成拼音
        例如：'新鲜水果' -> 'xin xian shui guo'（去除空格后为 'xinxianshuiguo'）
        """
        if self.ttitle and not self.ttitle_pinyin:
            # Style.NORMAL 表示普通拼音风格，不带声调
            self.ttitle_pinyin = ''.join(lazy_pinyin(self.ttitle, style=Style.NORMAL))
        super().save(*args, **kwargs)


class GoodsInfo(models.Model):
    """
    商品信息模型
    
    字段说明：
    - isDelete: 逻辑删除标识
    - gtitle: 商品名称
    - gtitle_pinyin: [新增] 商品名称拼音（如：caomei）
    - gtitle_pinyin_abbr: [新增] 商品名称拼音首字母（如：cm）
    - gtitle_en: [新增] 商品英文名称（如：strawberry）
    - gpic: 商品图片
    - gprice: 商品价格
    - gunit: 单位重量
    - gclick: 点击量
    - gjianjie: 商品简介
    - gjianjie_pinyin: [新增] 简介拼音
    - gkucun: 库存
    - gcontent: 商品详情（富文本）
    - gtype: 商品分类（外键关联TypeInfo）
    """
    isDelete = models.BooleanField(default=False)
    gtitle = models.CharField(max_length=20, verbose_name="商品名称", unique=True)
    # [新增] 商品名称拼音字段，支持拼音全拼搜索（如：caomei -> 草莓）
    gtitle_pinyin = models.CharField(max_length=100, verbose_name="商品拼音", blank=True, default='')
    # [新增] 商品名称拼音首字母字段，支持首字母搜索（如：cm -> 草莓）
    gtitle_pinyin_abbr = models.CharField(max_length=50, verbose_name="商品拼音首字母", blank=True, default='')
    # [新增] 商品英文名称字段，支持英文搜索（如：strawberry -> 草莓）
    gtitle_en = models.CharField(max_length=100, verbose_name="商品英文名", blank=True, default='')
    gpic = models.ImageField(verbose_name='商品图片', upload_to='df_goods/image/%Y/%m', null=True, blank=True)
    gprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="商品价格")
    gunit = models.CharField(max_length=20, default='500g', verbose_name="单位重量")
    gclick = models.IntegerField(verbose_name="点击量", default=0, null=False)
    gjianjie = models.CharField(max_length=200, verbose_name="简介")
    # [新增] 商品简介拼音字段，支持简介内容的拼音搜索
    gjianjie_pinyin = models.CharField(max_length=300, verbose_name="简介拼音", blank=True, default='')
    gkucun = models.IntegerField(verbose_name="库存", default=0)
    gcontent = HTMLField(max_length=200, verbose_name="详情")
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE, verbose_name="分类")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.gtitle

    def save(self, *args, **kwargs):
        """
        [新增] 重写保存方法，自动生成拼音字段
        
        当保存商品时，自动根据中文名称生成：
        1. 拼音全拼：'草莓' -> 'caomei'
        2. 拼音首字母：'草莓' -> 'cm'
        3. 简介拼音：用于简介内容的拼音搜索
        """
        if self.gtitle:
            # Style.NORMAL 生成完整拼音，如 '草莓' -> ['cao', 'mei'] -> 'caomei'
            self.gtitle_pinyin = ''.join(lazy_pinyin(self.gtitle, style=Style.NORMAL))
            # Style.FIRST_LETTER 生成首字母，如 '草莓' -> ['c', 'm'] -> 'cm'
            self.gtitle_pinyin_abbr = ''.join(lazy_pinyin(self.gtitle, style=Style.FIRST_LETTER))
        # 生成简介拼音，用于搜索简介内容
        if self.gjianjie and not self.gjianjie_pinyin:
            self.gjianjie_pinyin = ''.join(lazy_pinyin(self.gjianjie, style=Style.NORMAL))
        super().save(*args, **kwargs)
