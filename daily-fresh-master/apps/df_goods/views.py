from django.core.paginator import Paginator
from django.shortcuts import render

from df_user.models import UserInfo
from .models import GoodsInfo, TypeInfo
from df_cart.models import CartInfo
from df_user.models import GoodsBrowser
from elasticsearch import Elasticsearch
from django.conf import settings


def index(request):
    # 查询各个分类的最新4条，最热4条数据
    typelist = TypeInfo.objects.all()
    #  _set 连表操作
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]  # 按照上传顺序
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]  # 按照点击量
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
    # if request.session.has_key('user_id'):
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
    # tid：商品种类信息  pindex：商品页码 sort：商品显示分类方式
    typeinfo = TypeInfo.objects.get(pk=int(tid))

    # 根据主键查找当前的商品分类  海鲜或者水果
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # list.html左侧最新商品推荐
    goods_list = []
    # list中间栏商品显示方式
    cart_num, guest_cart = 0, 0

    try:
        user_id = request.session['user_id']
    except:
        user_id = None
    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    if sort == '1':  # 默认最新
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':  # 按照价格
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':  # 按照人气点击量
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    # 创建Paginator一个分页对象
    paginator = Paginator(goods_list, 4)
    # 返回Page对象，包含商品信息
    page = paginator.page(int(pindex))
    context = {
        'title': '商品列表',
        'guest_cart': guest_cart,
        'cart_num': cart_num,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,  # 排序方式
        'news': news,
    }
    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    good_id = gid
    goods = GoodsInfo.objects.get(pk=int(good_id))
    goods.gclick = goods.gclick + 1  # 商品点击量
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

    if 'user_id' in request.session:
        user_id = request.session["user_id"]
        try:
            browsed_good = GoodsBrowser.objects.get(user_id=int(user_id), good_id=int(good_id))
        except Exception:
            browsed_good = None
        if browsed_good:
            from datetime import datetime
            browsed_good.browser_time = datetime.now()
            browsed_good.save()
        else:
            GoodsBrowser.objects.create(user_id=int(user_id), good_id=int(good_id))
            browsed_goods = GoodsBrowser.objects.filter(user_id=int(user_id))
            browsed_good_count = browsed_goods.count()
            if browsed_good_count > 5:
                ordered_goods = browsed_goods.order_by("-browser_time")
                for _ in ordered_goods[5:]:
                    _.delete()
    return response


def cart_count(request):
    if 'user_id' in request.session:
        return CartInfo.objects.filter(user_id=request.session['user_id']).count
    else:
        return 0


# def ordinary_search(request):

#     from django.db.models import Q

#     search_keywords = request.GET.get('q', '')
#     pindex = request.GET.get('pindex', 1)
#     search_status = 1
#     cart_num, guest_cart = 0, 0

#     try:
#         user_id = request.session['user_id']
#     except:
#         user_id = None

#     if user_id:
#         guest_cart = 1
#         cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

#     goods_list = GoodsInfo.objects.filter(
#         Q(gtitle__icontains=search_keywords) |
#         Q(gcontent__icontains=search_keywords) |
#         Q(gjianjie__icontains=search_keywords)).order_by("gclick")

#     if goods_list.count() == 0:
#         # 商品搜索结果为空，返回推荐商品
#         search_status = 0
#         goods_list = GoodsInfo.objects.all().order_by("gclick")[:4]

#     paginator = Paginator(goods_list, 4)
#     page = paginator.page(int(pindex))

#     context = {
#         'title': '搜索列表',
#         'search_status': search_status,
#         'guest_cart': guest_cart,
#         'cart_num': cart_num,
#         'page': page,
#         'paginator': paginator,
#     }
#     return render(request, 'df_goods/ordinary_search.html', context)


def ordinary_search(request):
    """
    基于Elasticsearch的商品搜索功能
    
    功能特点：
    1. 支持多字段模糊搜索（商品名称、简介、详情）
    2. 支持中文分词（IK分词器）
    3. 支持相关性评分排序
    4. 支持分页展示
    
    Args:
        request: HTTP请求对象
        
    Returns:
        渲染后的搜索结果页面
    """
    from django.db.models import Q
    
    # ==================== 参数初始化 ====================
    # 获取搜索关键词，默认为空字符串
    search_keywords = request.GET.get('q', '')
    # 获取当前页码，默认为第1页
    page_num = int(request.GET.get('page', 1))
    # 每页显示的商品数量
    page_size = 4
    # 搜索状态标识：1=有搜索结果，0=无搜索结果
    search_status = 1
    # 购物车商品数量和购物车显示标识
    cart_num, guest_cart = 0, 0

    # ==================== 用户信息获取 ====================
    # 尝试从session中获取当前登录用户的ID
    try:
        user_id = request.session['user_id']
    except:
        user_id = None

    # 如果用户已登录，获取购物车商品数量
    if user_id:
        guest_cart = 1  # 显示购物车
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    # ==================== 搜索结果容器初始化 ====================
    # 存储搜索结果商品列表
    goods_list = []
    # 搜索结果总数
    total_count = 0
    # 存储高亮片段，key为商品ID，value为高亮字段字典（已禁用高亮功能）
    # highlights = {}

    # ==================== Elasticsearch搜索逻辑 ====================
    if search_keywords:
        try:
            # 创建ES客户端连接，从settings中读取ES服务器地址
            es = Elasticsearch(hosts=[settings.ELASTICSEARCH_DSL['default']['hosts']])
            
            # 构建ES搜索请求
            response = es.search(
                index='goods',  # 索引名称
                body={
                    # 查询条件
                    'query': {
                        'multi_match': {
                            'query': search_keywords,  # 搜索关键词
                            # 搜索字段及权重：gtitle权重3，gjianjie权重2，gcontent权重1
                            # ^符号表示权重提升，数值越大权重越高
                            'fields': ['gtitle^3', 'gjianjie^2', 'gcontent'],
                            # best_fields: 取最佳匹配字段的得分
                            'type': 'best_fields',
                            # 使用IK智能分词器进行中文分词
                            'analyzer': 'ik_smart'
                        }
                    },
                    # 高亮配置（已禁用）
                    # 'highlight': {
                    #     'fields': {
                    #         'gtitle': {},      # 商品名称高亮
                    #         'gjianjie': {},    # 商品简介高亮
                    #         'gcontent': {},    # 商品详情高亮
                    #     },
                    #     # 高亮标签，用于前端CSS样式
                    #     'pre_tags': ['<em class="highlight">'],
                    #     'post_tags': ['</em>'],
                    # },
                    # 分页参数：from表示偏移量，size表示每页数量
                    'from': (page_num - 1) * page_size,
                    'size': page_size,
                    # 排序规则：先按相关性得分降序，再按点击量降序
                    'sort': [
                        '_score',  # 相关性得分
                        {'gclick': {'order': 'desc'}}  # 点击量
                    ]
                }
            )

            # 解析搜索结果总数
            total_count = response['hits']['total']['value']
            
            # 遍历搜索结果，提取商品信息
            for hit in response['hits']['hits']:
                # 获取商品原始数据
                source = hit['_source']
                # 添加商品ID（ES中的文档ID）
                source['id'] = hit['_id']
                # 添加相关性得分，可用于排序展示
                source['score'] = hit['_score']
                
                # 高亮结果处理（已禁用）
                # if 'highlight' in hit:
                #     highlights[source['id']] = hit['highlight']
                
                # 将商品添加到结果列表
                goods_list.append(source)

            # 如果搜索结果为空，返回推荐商品
            if total_count == 0:
                search_status = 0  # 标记为无搜索结果
                # 从数据库获取点击量最高的4件商品作为推荐
                goods_list = list(GoodsInfo.objects.all().order_by('-gclick')[:4].values())
                
        except Exception as e:
            # ES搜索异常处理，打印详细错误日志并返回推荐商品
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
    # 创建分页器对象
    paginator = Paginator(goods_list, page_size)
    # 手动设置总数，用于正确计算总页数
    paginator._count = total_count if total_count > 0 else len(goods_list)
    # 获取当前页数据
    page = paginator.page(page_num)

    # ==================== 构建模板上下文 ====================
    context = {
        'title': '搜索列表',
        'search_status': search_status,    # 搜索状态
        'guest_cart': guest_cart,          # 是否显示购物车
        'cart_num': cart_num,              # 购物车商品数量
        'page': page,                      # 当前页数据
        'paginator': paginator,            # 分页器对象
        'query': search_keywords,          # 搜索关键词（用于前端显示）
        # 'highlights': highlights,        # 高亮结果字典（已禁用）
        'total_count': total_count,        # 搜索结果总数
    }
    return render(request, 'df_goods/ordinary_search.html', context)
    