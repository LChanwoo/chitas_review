from django.contrib import admin
from .models import Comment, Article

# Register your models here.



class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject','content', 'create_date']
    list_filter = ['create_date']

admin.site.register(Article, ArticleAdmin)

class CommentAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    list_display = ['id',  'article_id', 'create_date']
    list_filter = ['create_date']

admin.site.register(Comment, CommentAdmin)
