#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
天天生鲜项目数据库初始化脚本
使用pymysql库初始化MySQL数据库
"""

import pymysql
from pymysql import Error


class DatabaseInitializer:
    """数据库初始化类"""
    
    def __init__(self, host='localhost', port=3306, user='root', password='123456'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = 'daily_fresh'
        self.connection = None
    
    def create_database(self):
        """创建数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                charset='utf8mb4'
            )
            
            cursor = self.connection.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.database}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ 数据库 '{self.database}' 创建成功或已存在")
            
            cursor.execute(f"USE `{self.database}`")
            print(f"✓ 已切换到数据库 '{self.database}'")
            
        except Error as e:
            print(f"✗ 创建数据库失败: {e}")
            raise
        finally:
            if self.connection:
                self.connection.close()
    
    def get_connection(self):
        """获取数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            return self.connection
        except Error as e:
            print(f"✗ 连接数据库失败: {e}")
            raise
    
    def execute_sql_file(self):
        """执行SQL初始化脚本"""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            print("\n开始执行数据库初始化...")
            
            print("\n清空现有数据...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            tables = [
                'df_user_goodsbrowser',
                'df_order_orderdetailinfo',
                'df_order_orderinfo',
                'df_cart_cartinfo',
                'df_user_userinfo',
                'df_goods_goodsinfo',
                'df_goods_typeinfo',
            ]
            for table in tables:
                cursor.execute(f"TRUNCATE TABLE `{table}`")
                print(f"  ✓ 已清空表: {table}")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            print("  ✓ 已重新启用外键检查")
            
            print("\n[1/7] 初始化商品类型表...")
            typeinfo_data = [
                ('1', False, '新鲜水果'),
                ('2', False, '海鲜水产'),
                ('3', False, '猪羊牛肉'),
                ('4', False, '禽类蛋品'),
                ('5', False, '新鲜蔬菜'),
                ('6', False, '速冻食品'),
            ]
            cursor.executemany(
                "INSERT INTO df_goods_typeinfo (id, isDelete, ttitle) VALUES (%s, %s, %s)",
                typeinfo_data
            )
            print(f"  ✓ 插入 {len(typeinfo_data)} 条商品类型数据")
            
            print("\n[2/7] 初始化商品信息表...")
            goodsinfo_data = [
                ('1', False, '水晶葡萄', 'df_goods/image/2019/05/goods002_MDWYzFU.jpg', 20.00, '500g', 35, '好吃好吃真好吃', 504, '<p>好吃好吃真好吃&nbsp;好呀好呀真是好吃&nbsp;&nbsp;</p>', 1),
                ('2', False, '坷拉苹果', 'df_goods/image/2019/05/goods010_sCLUSfI.jpg', 20.00, '500g', 59, '好吃好吃真好吃', 445, '<h2 style="text-align: left;">好吃</h2>', 1),
                ('3', False, '奔跑的奇异果', 'df_goods/image/2019/05/goods012_fUad9Io.jpg', 100.00, '500g', 13, '好吃好吃真好吃', 497, '<p>好久啊啥的积分来扩大事件发酵速度；老放假；三闾大夫健康绿色的肌肤卡死机的；发就考虑对方</p>', 1),
                ('5', False, '酸死你柠檬', 'df_goods/image/2019/05/goods001_gxe2R45.jpg', 20.00, '500g', 56, '好吃好吃真好吃那是真好吃', 100, '<p>撒旦发生的范德萨阿阿迪发地方阿&nbsp; &nbsp;阿道夫阿萨德发的撒旦法阿斯蒂芬但是该打给发个&nbsp;</p>', 1),
                ('6', False, '花果山猕猴桃', 'df_goods/image/2019/05/goods012_YqqLqZ2.jpg', 15.00, '500g', 61, '孙悟空吃了拉肚子', 114, '<p>来自东升傲来国的神奇水果，花果山百年孕育而成，孙悟空吃了七十三变，长生养颜。</p>', 1),
                ('7', False, '香蕉大香蕉', 'df_goods/image/2019/05/goods009_2qlBjR9.jpg', 16.00, '500g', 1275, '来自东升傲来国的神奇水果，花果山百年孕育而成，孙悟空吃了七十三变，长生养颜。', 120, '<p>来自东升傲来国的神奇水果，花果山百年孕育而成，孙悟空吃了七十三变，长生养颜。</p>', 1),
                ('8', False, '橘子的诱惑', 'df_goods/image/2019/05/goods013_3Nynaeh.jpg', 26.00, '500g', 234, '来自东升傲来国的神奇水果，花果山百年孕育而成，孙悟空吃了七十三变，长生养颜。', 51, '<p>来自东升傲来国的神奇水果，花果山百年孕育而成，孙悟空吃了七十三变，长生养颜。</p>', 1),
                ('9', False, '大龙大龙虾', 'df_goods/image/2019/05/goods018_5ezSBcV.jpg', 50.00, '500g', 67, '海贼王强烈推荐', 89, '<p>吃了保证不拉肚子&nbsp;</p>', 2),
                ('10', False, '扇贝', 'df_goods/image/2019/05/goods019_KWeEVX7.jpg', 34.00, '500g', 147, '小龙女强烈推荐', 19, '<p>阿达那你还什么很尴尬身份个数是对方公司刚发的发</p>', 2),
                ('11', False, '濒危刀鱼', 'df_goods/image/2019/05/goods020_SmRaQgj.jpg', 100.00, '10g', 150, '这个贵', 1222, '<p>撒地方撒打算大三大四的风</p>', 2),
                ('12', False, '基围虾', 'df_goods/image/2019/05/goods021_HMsKKDV.jpg', 45.00, '500g', 70, '好吃好吃不上火', 29, '<p>嘎多吧反革命活动每天发生的 你</p>', 2),
                ('13', False, '大红草莓', 'df_goods/image/2019/05/goods003_QjVxM2e.jpg', 20.00, '500g', 109, '又大又红又好吃', 62, '<p><span style="color: #e4393c; font-family: tahoma, arial, \'Microsoft YaHei\', \'Hiragino Sans GB\', u5b8bu4f53, sans-serif; font-size: 12px;">爱你&ldquo;莓&rdquo;商量，鲜美红嫩，个大饱满，肉质细腻，轻咬一口，汁水充盈整个口腔</span></p>', 1),
                ('14', False, '樱桃', 'df_goods/image/2019/05/goods005_HkX6imN.jpg', 22.00, '500g', 283, '好吃好吃真好吃', 58, '<p><span style="color: #e4393c; font-family: tahoma, arial, \'Microsoft YaHei\', \'Hiragino Sans GB\', u5b8bu4f53, sans-serif; font-size: 12px;">鲜美红嫩，个大饱满，肉质细腻，轻咬一口，汁水充盈整个口腔，给你初恋般的美妙感觉！</span></p>', 1),
                ('15', False, '新鲜草莓', 'df_goods/image/2019/05/goods_detail_MMB8vJ4.jpg', 20.00, '500g', 271, '好吃到上heaven', 285, '<p>一口进医院，两口救活难</p>', 1),
                ('16', False, '海南香蕉', 'df_goods/image/2019/05/goods009_ECGyaM2.jpg', 100.00, '500g', 0, '海南香蕉海南香蕉', 122, '<p>海南香蕉海南香蕉海南香蕉海南香蕉海南香蕉</p>', 1),
                ('17', False, '来自海南的香蕉', 'df_goods/image/2019/05/goods009_1Y22XAV_Xkxl6mq.jpg', 89.00, '500g', 3, '海南香蕉海南香蕉', 314, '<p>来自海南的香蕉</p>', 1),
                ('18', False, '牛奶草莓', 'df_goods/image/2019/05/goods_detail.jpg', 12.00, '500g', 2, '阿萨德', 324, '<p>阿斯蒂芬阿三的说法</p>', 1),
            ]
            cursor.executemany(
                "INSERT INTO df_goods_goodsinfo (id, isDelete, gtitle, gpic, gprice, gunit, gclick, gjianjie, gkucun, gcontent, gtype_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                goodsinfo_data
            )
            print(f"  ✓ 插入 {len(goodsinfo_data)} 条商品信息数据")
            
            print("\n[3/7] 初始化用户信息表...")
            userinfo_data = [
                ('32', '111111', '3d4f2bf07dc1be38b20cd6e46949a1071f9d0e3d', '111111@163.com', '散人', '河南理工大学南校区', '477100', '13323232332'),
                ('33', 'sanren', '4569416a6a60a85332f52e25b096bec0be49060a', 'sanren@163.com', '散人', '112', '112', '112'),
                ('34', 'root2', '7b21848ac9af35be0ddb2d6b9fc3851934db8420', 'root2@163.com', '', '', '', ''),
                ('35', '11111', '7b21848ac9af35be0ddb2d6b9fc3851934db8420', '11111@163.com', '', '', '', ''),
                ('36', '22222', '1a9b9508b6003b68ddfe03a9c8cbc4bd4388339b', '22222@163.com', '', '', '', ''),
                ('37', '33333', '403d9917c3e950798601addf7ba82cd3c83f344b', '33333@163.com', '', '', '', ''),
                ('38', 'login', '2736fab291f04e69b62d490c3c09361f5b82461a', 'login@qq.com', '', '', '', ''),
                ('39', 'asdfg', 'f1b699cc9af3eeb98e5de244ca7802ae38e77bae', 'asdfg@qq.com', '', '', '', ''),
            ]
            cursor.executemany(
                "INSERT INTO df_user_userinfo (id, uname, upwd, uemail, ushou, uaddress, uyoubian, uphone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                userinfo_data
            )
            print(f"  ✓ 插入 {len(userinfo_data)} 条用户信息数据")
            
            print("\n[4/7] 初始化购物车表...")
            cartinfo_data = [
                ('61', 33, 9, 1),
                ('63', 33, 14, 4),
                ('66', 32, 12, 2),
                ('67', 39, 15, 1),
            ]
            cursor.executemany(
                "INSERT INTO df_cart_cartinfo (id, user_id, goods_id, count) VALUES (%s, %s, %s, %s)",
                cartinfo_data
            )
            print(f"  ✓ 插入 {len(cartinfo_data)} 条购物车数据")
            
            print("\n[5/7] 初始化订单信息表...")
            orderinfo_data = [
                ('2018122009332333', 33, '2018-12-20 09:33:23.769712', False, 36.00, ''),
                ('2018122009345533', 33, '2018-12-20 09:34:55.063443', False, 32.00, ''),
                ('2018122009352733', 33, '2018-12-20 09:35:27.226788', False, 30.00, ''),
                ('2018122009415333', 33, '2018-12-20 09:41:53.530804', False, 415.00, ''),
                ('2019042720141632', 32, '2019-04-27 20:14:16.245991', False, 70.00, ''),
                ('2019050121492832', 32, '2019-05-01 21:49:28.106780', False, 301.00, ''),
            ]
            cursor.executemany(
                "INSERT INTO df_order_orderinfo (oid, user_id, odate, oIsPay, ototal, oaddress) VALUES (%s, %s, %s, %s, %s, %s)",
                orderinfo_data
            )
            print(f"  ✓ 插入 {len(orderinfo_data)} 条订单信息数据")
            
            print("\n[6/7] 初始化订单详情表...")
            orderdetail_data = [
                ('1', 8, '2018122009332333', 26.00, 1),
                ('2', 14, '2018122009345533', 22.00, 1),
                ('3', 13, '2018122009352733', 20.00, 1),
                ('4', 12, '2018122009415333', 45.00, 9),
                ('5', 15, '2019042720141632', 20.00, 3),
                ('6', 18, '2019050121492832', 12.00, 2),
                ('7', 17, '2019050121492832', 89.00, 3),
            ]
            cursor.executemany(
                "INSERT INTO df_order_orderdetailinfo (id, goods_id, order_id, price, count) VALUES (%s, %s, %s, %s, %s)",
                orderdetail_data
            )
            print(f"  ✓ 插入 {len(orderdetail_data)} 条订单详情数据")
            
            print("\n[7/7] 初始化用户浏览记录表...")
            goodsbrowser_data = [
                ('17', 33, 14, '2018-12-23 20:46:05.525349'),
                ('18', 33, 12, '2018-12-20 09:41:32.140375'),
                ('19', 33, 13, '2018-12-20 09:35:19.361044'),
                ('20', 33, 9, '2018-12-20 09:43:13.196705'),
                ('21', 33, 15, '2018-12-23 20:48:52.036342'),
                ('22', 32, 15, '2019-04-05 18:22:13.755243'),
                ('24', 32, 5, '2019-05-04 13:24:11.707059'),
                ('25', 32, 17, '2019-05-01 21:49:19.037944'),
                ('26', 32, 18, '2019-05-01 21:49:11.835061'),
                ('27', 32, 12, '2019-05-04 13:24:35.371517'),
                ('28', 39, 18, '2019-05-12 22:05:00.881861'),
            ]
            cursor.executemany(
                "INSERT INTO df_user_goodsbrowser (id, user_id, good_id, browser_time) VALUES (%s, %s, %s, %s)",
                goodsbrowser_data
            )
            print(f"  ✓ 插入 {len(goodsbrowser_data)} 条用户浏览记录数据")
            
            connection.commit()
            print("\n" + "="*50)
            print("✓ 数据库初始化完成！")
            print("="*50)
            
        except Error as e:
            print(f"\n✗ 执行SQL失败: {e}")
            connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
    
    def initialize(self):
        """执行完整的数据库初始化流程"""
        print("="*50)
        print("天天生鲜项目数据库初始化")
        print("="*50)
        print(f"数据库主机: {self.host}:{self.port}")
        print(f"数据库用户: {self.user}")
        print(f"数据库名称: {self.database}")
        print("="*50)
        
        self.create_database()
        self.execute_sql_file()


def main():
    """主函数"""
    try:
        initializer = DatabaseInitializer(
            host='localhost',
            port=3306,
            user='root',
            password='123456'
        )
        initializer.initialize()
    except Exception as e:
        print(f"\n✗ 初始化失败: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
