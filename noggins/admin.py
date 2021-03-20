from django.contrib import admin

# Register your models here.
from .models import Noggin, NogginLike, Comment, NogginEyeball

class NogginLikeAdmin(admin.TabularInline):
    model = NogginLike
    

class NogginViewAdmin(admin.TabularInline):
    model = NogginEyeball

class NogginCommentAdmin(admin.TabularInline):
    model = Comment

class NogginAdmin(admin.ModelAdmin):
    inlines = [NogginLikeAdmin, NogginCommentAdmin, NogginViewAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content','user__username','user__email']
    class Meta:
        model = Noggin

admin.site.register(Noggin, NogginAdmin)

