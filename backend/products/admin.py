from django.contrib import admin

from products import models


class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','category','brand']
    readonly_fields=['image']

class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']

class BrandAdmin(admin.ModelAdmin):
    list_display=['id','name']

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user']

class CommentAdmin(admin.ModelAdmin):
    list_display=['id','user','product','reply_to']

admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Brand,BrandAdmin)
admin.site.register(models.Order,OrderAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.OrderItem)


