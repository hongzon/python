from django.contrib import admin

from .models import Teacher, Subject, User, Membership, TaggedItem


class UserAdmin(admin.ModelAdmin):
    list_display = ('no', 'username', 'email', 'counter')
    ordering = ('no', )
class MembershipInline(admin.TabularInline):
    model = Teacher.subject.through
    # model = Membership
    # extra = 1

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'intro')
    ordering = ('no', )


class TeacherAdmin(admin.ModelAdmin):
    # exclude = ('subject',)
    list_display = ('no', 'name', 'intro', 'motto', 'manager')
    search_fields = ('name', 'intro')
    ordering = ('no', )
    # inlines = [
    #     MembershipInline,
    # ]
    filter_vertical = ('subject',)
class TaggedItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(TaggedItem, TaggedItemAdmin)
