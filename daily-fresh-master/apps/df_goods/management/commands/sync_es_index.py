"""
Elasticsearch 索引同步管理命令

本模块提供 Django 管理命令，用于手动同步商品数据到 Elasticsearch。
可通过 python manage.py sync_es_index 命令执行。

主要功能：
1. 删除现有索引
2. 创建新索引（包含正确的映射配置）
3. 同步所有商品数据到 ES
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
from django_elasticsearch_dsl.registries import registry


class Command(BaseCommand):
    """
    同步商品数据到 Elasticsearch 的管理命令
    
    使用方法：
        python manage.py sync_es_index
    
    执行流程：
        1. 初始化 ES 连接
        2. 删除现有索引（如果存在）
        3. 创建新索引（根据 documents.py 中的定义，包含映射）
        4. 遍历所有已注册的文档类型
        5. 将数据库数据同步到 ES 索引
    """
    
    # 命令帮助信息
    help = '同步商品数据到 Elasticsearch'

    def handle(self, *args, **options):
        """
        命令执行入口
        
        Args:
            *args: 位置参数
            **options: 命令选项
            
        执行步骤：
            1. 初始化连接
            2. 删除旧索引
            3. 创建新索引（包含映射）
            4. 同步数据
        """
        # 步骤1：初始化 Elasticsearch 连接
        self.stdout.write('初始化 Elasticsearch 连接...')
        
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
        
        self.stdout.write(f'已连接到 Elasticsearch: {hosts}')
        
        # 步骤2：创建索引（包含正确的映射配置）
        self.stdout.write('开始创建索引...')
        
        for doc in registry.get_documents():
            # 获取索引对象
            index = doc._index
            index_name = index._name
            
            # 如果索引存在则删除
            if es_client.indices.exists(index=index_name):
                es_client.indices.delete(index=index_name)
                self.stdout.write(f'已删除索引: {index_name}')
            
            # 创建索引定义（包含映射和设置）
            index_body = {
                'settings': {
                    'number_of_shards': 1,
                    'number_of_replicas': 0,
                    'analysis': {
                        'analyzer': {
                            'ik_smart': {
                                'type': 'custom',
                                'tokenizer': 'ik_smart'
                            },
                            'ik_max_word': {
                                'type': 'custom',
                                'tokenizer': 'ik_max_word'
                            }
                        }
                    }
                },
                'mappings': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'isDelete': {'type': 'boolean'},
                        'gtitle': {
                            'type': 'text',
                            'analyzer': 'ik_max_word',
                            'search_analyzer': 'ik_smart',
                            'fields': {
                                'raw': {'type': 'keyword'}
                            }
                        },
                        'gjianjie': {
                            'type': 'text',
                            'analyzer': 'ik_max_word',
                            'search_analyzer': 'ik_smart'
                        },
                        'gcontent': {
                            'type': 'text',
                            'analyzer': 'ik_max_word',
                            'search_analyzer': 'ik_smart'
                        },
                        'gprice': {'type': 'float'},
                        'gpic': {'type': 'keyword'},
                        'gclick': {'type': 'integer'},
                        'gkucun': {'type': 'integer'},
                        'gunit': {'type': 'keyword'},
                        'gtype': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'ttitle': {
                                    'type': 'text',
                                    'analyzer': 'ik_smart'
                                }
                            }
                        }
                    }
                }
            }
            
            # 创建新索引
            es_client.indices.create(index=index_name, body=index_body)
            self.stdout.write(f'已创建索引（包含IK分词器映射）: {index_name}')
        
        # 步骤3：同步数据
        self.stdout.write('开始同步数据...')
        
        # 遍历所有已注册的文档类
        for doc in registry.get_documents():
            # 获取关联的 Django 模型
            model = doc.Django.model
            # 获取所有需要同步的数据
            queryset = model.objects.all()
            
            # 批量同步数据
            doc_instance = doc()
            success_count = 0
            for obj in queryset:
                try:
                    doc_instance.update(obj)
                    success_count += 1
                except Exception as e:
                    self.stdout.write(f'同步失败 [{obj}]: {e}')
            
            self.stdout.write(f'已同步 {success_count}/{queryset.count()} 条数据到: {doc.__name__}')
        
        # 输出成功信息
        self.stdout.write(self.style.SUCCESS('同步完成!'))
