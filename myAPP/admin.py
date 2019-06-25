from django.contrib import admin
from .models import employees,departments,overtimes,arrangements,attendances,leaves,managers,over_list

# Register your models here.
# class EmployeesAdmin(admin.ModelAdmin):
#     #列表页属性
#     list_display=['id','name','password']#显示字段
#     list_filter=['name']#过滤器，过滤条件的
#     search_fields=['name']#可以按gname搜索
#     list_per_page=5#分页
#
#     #修改添加页属性
#     fields=['department_id','arrange_id']#规定属性先后顺序

admin.site.register(employees)
admin.site.register(departments)
admin.site.register(arrangements)
admin.site.register(attendances)
admin.site.register(leaves)
admin.site.register(managers)
admin.site.register(over_list)
admin.site.register(overtimes)
