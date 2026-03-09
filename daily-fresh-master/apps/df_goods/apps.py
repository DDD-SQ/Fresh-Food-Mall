from django.apps import AppConfig


class DfGoodsConfig(AppConfig):
    name = 'df_goods'
    verbose_name = "商品"

    def ready(self):
        """
        应用启动时执行的操作
        
        功能：
        1. 导入信号模块，确保信号处理器被注册
        2. 导入文档模块，确保 ES 文档被注册
        3. 初始化 Elasticsearch 连接
        """
        # 导入信号模块，确保 ES 索引自动同步信号生效
        import df_goods.signals  # noqa
        # 导入文档模块，确保 ES 文档映射被注册
        import df_goods.documents  # noqa
        
        # 初始化 Elasticsearch 连接
        self._init_elasticsearch_connection()

    def _init_elasticsearch_connection(self):
        """
        初始化 Elasticsearch 连接
        
        在应用启动时配置 elasticsearch-dsl 的默认连接，
        确保信号处理器能够正常访问 ES。
        """
        try:
            from django.conf import settings
            from elasticsearch import Elasticsearch
            from elasticsearch_dsl import connections
            
            es_config = settings.ELASTICSEARCH_DSL.get('default', {})
            hosts = es_config.get('hosts', 'http://localhost:9200')
            http_auth = es_config.get('http_auth')
            timeout = es_config.get('timeout', 30)
            
            # 创建 ES 客户端连接
            es_client = Elasticsearch(
                hosts=[hosts],
                http_auth=http_auth,
                timeout=timeout,
            )
            
            # 配置 elasticsearch-dsl 连接
            connections.add_connection('default', es_client)
        except Exception as e:
            # 连接失败时不影响应用启动，仅打印警告
            import warnings
            warnings.warn(f'Elasticsearch 连接初始化失败: {e}')
