from django.contrib import admin

from habrparser.models import Article, Hub


class HubAdmin(admin.ModelAdmin):
    pass


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Hub, HubAdmin)
admin.site.register(Article, ArticleAdmin)
