from django.contrib import admin
from .models import Post, Comment, Like, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Количество пустых форм для добавления новых изображений

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at')  # Поля, которые будут отображаться в списке
    search_fields = ('text',)  # Поля, по которым можно будет искать
    inlines = [ImageInline]  # Встраиваемая модель для изображений

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('text',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')

# Регистрация моделей в админке
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Image)
