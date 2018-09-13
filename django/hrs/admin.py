from django.contrib import admin

from hrs.models import Emp, Dept


class DeptAdmin(admin.ModelAdmin):

    list_display = ('no', 'name', 'location')
    ordering = ('no', )
    search_fields = ('name',)


class EmpAdmin(admin.ModelAdmin):

    list_display = ('no', 'name', 'job', 'mgr', 'sal', 'comm', 'dept')
    search_fields = ('name', 'job')
    list_select_related = ('dept',)
    raw_id_fields = ("dept",)


admin.site.register(Dept, DeptAdmin)
admin.site.register(Emp, EmpAdmin)