from django.db import models
from django.contrib import admin
from MessageModel.models import WarningMessage
from django.utils.safestring import mark_safe

# Blog模型的管理器
@admin.register(WarningMessage)
class WarningMessageAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('describe', 'face_img', 'create_date_time')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-create_date_time',)

    date_hierarchy = 'create_date_time'  # 详细时间分层筛选　

    readonly_fields = ('face',)  # 必须加这行 否则访问编辑页面会报错

    def face_img(self, obj):
        #print(obj.face.url)
        return mark_safe(u'<img src="%s" width="100px" />' % obj.face.url)

    # 页面显示的字段名称
    face_img.short_description = u'面部照片'







