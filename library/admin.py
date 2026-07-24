from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, CourseFile


class CustomUserAdmin(UserAdmin):
    """
    UserAdmin مخصص يضيف الحقول الإضافية بتاعتنا (user_type, student_id, full_name, is_frozen)
    ويحافظ على تشفير كلمة المرور تلقائياً زي الأصل بتاع Django.

    ملاحظة مهمة: صفحة /admin دي مقصورة أصلاً على أي مستخدم عنده is_staff=True.
    البروفيسورات (ADMIN) والطلاب بيتم إنشاؤهم بـ is_staff=False دايماً (شوف views.py)،
    فمش هيقدروا يدخلوا هنا حتى لو حد غلط وحاول. الروت بس هو اللي عنده is_staff=True.
    """
    model = User

    list_display = ('username', 'full_name', 'user_type', 'student_id', 'is_frozen', 'is_staff')
    list_filter = ('user_type', 'is_frozen', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('بيانات إضافية', {'fields': ('user_type', 'student_id', 'full_name', 'is_frozen', 'frozen_until')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('بيانات إضافية', {'fields': ('user_type', 'student_id', 'full_name', 'is_frozen')}),
    )

    search_fields = ('username', 'full_name', 'student_id')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(CourseFile)
