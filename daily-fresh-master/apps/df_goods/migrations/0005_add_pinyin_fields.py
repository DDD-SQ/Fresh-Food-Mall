"""
数据库迁移文件：添加拼音和英文字段

本迁移文件为 TypeInfo 和 GoodsInfo 模型添加以下字段：
1. ttitle_pinyin: 分类名称拼音
2. ttitle_en: 分类英文名称
3. gtitle_pinyin: 商品名称拼音
4. gtitle_pinyin_abbr: 商品名称拼音首字母
5. gtitle_en: 商品英文名称
6. gjianjie_pinyin: 商品简介拼音

这些字段用于支持：
- 拼音搜索（如：caomei -> 草莓）
- 拼音首字母搜索（如：cm -> 草莓）
- 英文搜索（如：strawberry -> 草莓）
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    数据库迁移类
    
    依赖：df_goods.0004_auto_20260227_1619
    操作：添加6个新字段
    """

    dependencies = [
        ('df_goods', '0004_auto_20260227_1619'),
    ]

    operations = [
        # [新增] TypeInfo 模型 - 分类拼音字段
        migrations.AddField(
            model_name='typeinfo',
            name='ttitle_pinyin',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='分类拼音'),
        ),
        # [新增] TypeInfo 模型 - 分类英文名称字段
        migrations.AddField(
            model_name='typeinfo',
            name='ttitle_en',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='分类英文名'),
        ),
        # [新增] GoodsInfo 模型 - 商品名称拼音字段（支持拼音全拼搜索）
        migrations.AddField(
            model_name='goodsinfo',
            name='gtitle_pinyin',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='商品拼音'),
        ),
        # [新增] GoodsInfo 模型 - 商品名称拼音首字母字段（支持首字母搜索）
        migrations.AddField(
            model_name='goodsinfo',
            name='gtitle_pinyin_abbr',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='商品拼音首字母'),
        ),
        # [新增] GoodsInfo 模型 - 商品英文名称字段（支持英文搜索）
        migrations.AddField(
            model_name='goodsinfo',
            name='gtitle_en',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='商品英文名'),
        ),
        # [新增] GoodsInfo 模型 - 商品简介拼音字段
        migrations.AddField(
            model_name='goodsinfo',
            name='gjianjie_pinyin',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='简介拼音'),
        ),
    ]
