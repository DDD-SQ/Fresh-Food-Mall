"""
商品视图模块

本模块提供商品相关的视图函数，包括首页、列表页、详情页和搜索功能。

主要功能：
1. 商品首页展示
2. 商品列表页（分类、排序、分页）
3. 商品详情页
4. [新增] 增强版搜索功能（支持拼音、英文、模糊搜索等）
"""

from django.core.paginator import Paginator
from django.shortcuts import render

from df_user.models import UserInfo
from .models import GoodsInfo, TypeInfo
from df_cart.models import CartInfo
from df_user.models import GoodsBrowser
from elasticsearch import Elasticsearch
from django.conf import settings
# [新增] 导入正则表达式模块，用于判断输入是否为拼音
import re


def index(request):
    """
    首页视图函数
    
    展示各个分类的最新4条和最热4条商品数据
    """
    typelist = TypeInfo.objects.all()
    # 获取各分类的最新商品（按上传顺序）
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]  # 按点击量
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    cart_num = 0
    # 判断是否存在登录状态
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': '首页',
        'cart_num': cart_num,
        'guest_cart': 1,
        'type0': type0, 'type01': type01,
        'type1': type1, 'type11': type11,
        'type2': type2, 'type21': type21,
        'type3': type3, 'type31': type31,
        'type4': type4, 'type41': type41,
        'type5': type5, 'type51': type51,
    }

    return render(request, 'df_goods/index.html', context)


def good_list(request, tid, pindex, sort):
    """
    商品列表视图函数
    
    Args:
        tid: 商品种类ID
        pindex: 商品页码
        sort: 商品显示分类方式（1=最新，2=价格，3=人气）
    """
    typeinfo = TypeInfo.objects.get(pk=int(tid))

    # list.html左侧最新商品推荐
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    goods_list = []
    cart_num, guest_cart = 0, 0

    try:
        user_id = request.session['user_id']
    except:
        user_id = None
    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    # 根据排序方式获取商品列表
    if sort == '1':  # 默认最新
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':  # 按照价格
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':  # 按照人气点击量
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    # 创建Paginator分页对象
    paginator = Paginator(goods_list, 4)
    page = paginator.page(int(pindex))
    context = {
        'title': '商品列表',
        'guest_cart': guest_cart,
        'cart_num': cart_num,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,
        'news': news,
    }
    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    """
    商品详情视图函数
    
    Args:
        gid: 商品ID
    """
    good_id = gid
    goods = GoodsInfo.objects.get(pk=int(good_id))
    goods.gclick = goods.gclick + 1  # 商品点击量+1
    goods.save()

    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title': goods.gtype.ttitle,
        'guest_cart': 1,
        'cart_num': cart_count(request),
        'goods': goods,
        'news': news,
        'id': good_id,
    }
    response = render(request, 'df_goods/detail.html', context)

    # 记录用户浏览历史
    if 'user_id' in request.session:
        user_id = request.session["user_id"]
        try:
            browsed_good = GoodsBrowser.objects.get(user_id=int(user_id), good_id=int(good_id))
        except Exception:
            browsed_good = None
        if browsed_good:
            # 更新浏览时间
            from datetime import datetime
            browsed_good.browser_time = datetime.now()
            browsed_good.save()
        else:
            # 新增浏览记录
            GoodsBrowser.objects.create(user_id=int(user_id), good_id=int(good_id))
            browsed_goods = GoodsBrowser.objects.filter(user_id=int(user_id))
            browsed_good_count = browsed_goods.count()
            # 最多保留5条浏览记录
            if browsed_good_count > 5:
                ordered_goods = browsed_goods.order_by("-browser_time")
                for _ in ordered_goods[5:]:
                    _.delete()
    return response


def cart_count(request):
    """获取购物车商品数量"""
    if 'user_id' in request.session:
        return CartInfo.objects.filter(user_id=request.session['user_id']).count
    else:
        return 0


# ==================== [新增] 搜索相关辅助函数 ====================

def is_pinyin(text):
    """
    [新增] 判断输入是否为拼音（纯字母）
    
    用于区分用户输入的是中文还是拼音，以便采用不同的搜索策略。
    
    Args:
        text: 用户输入的搜索关键词
        
    Returns:
        bool: 如果是纯字母返回True，否则返回False
        
    Examples:
        >>> is_pinyin('caomei')
        True
        >>> is_pinyin('草莓')
        False
    """
    return bool(re.match(r'^[a-zA-Z]+$', text))


def build_search_query(search_keywords):
    """
    [新增] 构建增强的ES搜索查询
    
    根据用户输入的关键词类型，构建不同的ES查询语句。
    支持多种搜索场景：
    
    1. 拼音首字母搜索（输入长度<=4的纯字母）
       例如：'cm' -> 草莓、'sg' -> 水果
       
    2. 拼音全拼搜索（输入长度>4的纯字母）
       例如：'caomei' -> 草莓、'shuiguo' -> 水果
       
    3. 英文名称搜索（输入较长的纯字母，可能是英文）
       例如：'strawberry' -> 草莓
       
    4. 中文搜索（包含中文的关键词）
       支持模糊匹配、分类关联、多关键词筛选
       
    Args:
        search_keywords: 用户输入的搜索关键词
        
    Returns:
        dict: ES查询语句字典
    """
    # 将关键词按空格分割，支持多关键词搜索
    keywords = search_keywords.split()
    
    # ==================== 拼音搜索逻辑 ====================
    if is_pinyin(search_keywords):
        # 短拼音（<=4个字符）：优先匹配拼音首字母
        if len(search_keywords) <= 4:
            return {
                'bool': {
                    'should': [
                        {
                            'term': {
                                'gtitle_pinyin_abbr': {
                                    'value': search_keywords.lower(),
                                    'boost': 3.0
                                }
                            }
                        },
                        {
                            'match': {
                                'gtitle_pinyin': {
                                    'query': search_keywords,
                                    'boost': 2.0
                                }
                            }
                        },
                        {
                            'match': {
                                'gtype.ttitle_pinyin': {
                                    'query': search_keywords,
                                    'boost': 1.5
                                }
                            }
                        }
                    ]
                }
            }
        # 长拼音（>4个字符）：匹配拼音全拼或英文
        else:
            return {
                'bool': {
                    'should': [
                        # 英文名称精确匹配（权重最高）
                        {
                            'term': {
                                'gtitle_en': {
                                    'value': search_keywords.lower(),
                                    'boost': 5.0
                                }
                            }
                        },
                        # 拼音全拼匹配
                        {
                            'match': {
                                'gtitle_pinyin': {
                                    'query': search_keywords,
                                    'boost': 3.0
                                }
                            }
                        },
                        # 分类拼音匹配
                        {
                            'match': {
                                'gtype.ttitle_pinyin': {
                                    'query': search_keywords,
                                    'boost': 2.0
                                }
                            }
                        }
                    ]
                }
            }
    
    # ==================== 中文搜索逻辑 ====================
    # 构建多字段搜索条件
    should_clauses = []
    
    for keyword in keywords:
        keyword_clauses = [
            # 匹配商品名称（带模糊匹配，支持错别字）
            {
                'match': {
                    'gtitle': {
                        'query': keyword,
                        'boost': 4.0,           # 商品名称权重最高
                        'fuzziness': 'AUTO',    # 自动模糊匹配，支持错别字
                        'minimum_should_match': '75%'  # 至少匹配75%的字符
                    }
                }
            },
            # 匹配商品名称关键词字段（用于模糊匹配）
            {
                'match': {
                    'gtitle.keyword': {
                        'query': keyword,
                        'boost': 3.5,
                        'fuzziness': 1  # 允许1个字符的差异
                    }
                }
            },
            # 匹配分类名称（支持分类关联搜索）
            {
                'match': {
                    'gtype.ttitle': {
                        'query': keyword,
                        'boost': 3.0  # 分类匹配权重较高
                    }
                }
            },
            # 匹配商品拼音（支持中文输入时也能匹配拼音）
            {
                'match': {
                    'gtitle_pinyin': {
                        'query': keyword,
                        'boost': 2.5
                    }
                }
            },
            # 匹配英文名称
            {
                'term': {
                    'gtitle_en': {
                        'value': keyword.lower(),
                        'boost': 4.0,
                        'case_insensitive': True
                    }
                }
            }
        ]
        should_clauses.extend(keyword_clauses)
    
    # 返回组合查询
    # minimum_should_match: 必须至少匹配一个关键词的所有条件
    return {
        'bool': {
            'should': should_clauses,
            'minimum_should_match': len(keywords)
        }
    }


def ordinary_search(request):
    """
    
    功能特点：
    1. 模糊搜索：草莓 -> XX草莓、草莓XX
    2. 分类关联搜索：水果 -> 该分类下所有商品
    3. 联想词搜索：莓 -> 草莓、蓝莓
    4. 多重筛选：进口 蓝莓 -> 同时包含两个关键词的商品
    5. 错别字容错：草霉 -> 草莓
    6. 英文搜索：strawberry -> 草莓商品
    7. 拼音搜索：caomei -> 草莓商品
    
    请求参数：
        q: 搜索关键词
        page: 页码（默认为1）
        
    Returns:
        渲染后的搜索结果页面
    """
    from django.db.models import Q
    
    # ==================== 参数初始化 ====================
    search_keywords = request.GET.get('q', '').strip()  # 搜索关键词，去除首尾空格
    page_num = int(request.GET.get('page', 1))          # 当前页码
    page_size = 4                                        # 每页显示数量
    search_status = 1                                    # 搜索状态：1=有结果，0=无结果
    cart_num, guest_cart = 0, 0

    # ==================== 用户信息获取 ====================
    try:
        user_id = request.session['user_id']
    except:
        user_id = None

    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    # ==================== 搜索结果容器初始化 ====================
    goods_list = []
    total_count = 0

    # ==================== Elasticsearch搜索逻辑 ====================
    if search_keywords:
        try:
            # 创建ES客户端连接
            es = Elasticsearch(hosts=[settings.ELASTICSEARCH_DSL['default']['hosts']])
            
            # 构建搜索查询
            search_query = build_search_query(search_keywords)
            
            # 执行搜索 - 获取所有结果，在Django层面分页
            response = es.search(
                index='goods',
                body={
                    'query': search_query,
                    'from': 0,           # 从第一条开始
                    'size': 100,         # 获取足够多的数据（最多100条）
                    'sort': [
                        '_score',                          # 按相关性得分排序
                        {'gclick': {'order': 'desc'}}      # 按点击量降序
                    ],
                    'min_score': 0.1  # 最低相关性得分阈值
                }
            )

            # 解析搜索结果
            total_count = response['hits']['total']['value']
            
            for hit in response['hits']['hits']:
                source = hit['_source']
                source['id'] = hit['_id']       # 商品ID
                source['score'] = hit['_score'] # 相关性得分
                goods_list.append(source)

            # 如果搜索结果为空，返回推荐商品
            if total_count == 0:
                search_status = 0
                goods_list = list(GoodsInfo.objects.all().order_by('-gclick')[:4].values())
                
        except Exception as e:
            # ES搜索异常处理
            import traceback
            print(f"ES搜索异常: {e}")
            traceback.print_exc()
            search_status = 0
            goods_list = list(GoodsInfo.objects.all().order_by('-gclick')[:4].values())
    else:
        # 无搜索关键词时，返回推荐商品
        search_status = 0
        goods_list = list(GoodsInfo.objects.all().order_by('-gclick')[:4].values())


    # ==================== 分页处理 ====================
    paginator = Paginator(goods_list, page_size)
    page = paginator.page(page_num)

    # ==================== 构建模板上下文 ====================
    context = {
        'title': '搜索列表',
        'search_status': search_status,    # 搜索状态
        'guest_cart': guest_cart,          # 是否显示购物车
        'cart_num': cart_num,              # 购物车商品数量
        'page': page,                      # 当前页数据
        'paginator': paginator,            # 分页器对象
        'query': search_keywords,          # 搜索关键词
        'total_count': total_count,        # 搜索结果总数
    }
    return render(request, 'df_goods/ordinary_search.html', context)
