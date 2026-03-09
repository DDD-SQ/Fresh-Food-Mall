from django.contrib import admin
from django.urls import path
# from django.conf.urls import url, include
from django.views.static import serve  # 上传文件处理函数
from django.urls import re_path, include
from .settings import MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include('df_goods.urls', namespace='df_goods')),
    re_path(r'^user/', include('df_user.urls', namespace='df_user')),
    re_path(r'^cart/', include('df_cart.urls', namespace='df_cart')),
    re_path(r'^order/', include('df_order.urls', namespace='df_order')),
    re_path(r'^tinymce/', include('tinymce.urls')),  # 使用富文本编辑框配置confurl
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT})
]
