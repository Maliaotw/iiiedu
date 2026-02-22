from django.contrib import admin
from iiiedu import models


# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Branch)
admin.site.register(models.Tag)
admin.site.register(models.Cate)
admin.site.register(models.Course)
admin.site.register(models.Favorite)
admin.site.register(models.Reply)
admin.site.register(models.Role)
admin.site.register(models.Menu)
admin.site.register(models.Series)
admin.site.register(models.Theme)
