from django.contrib import admin
from .models import lkModel,lkModelType
# Register your models here.

@admin.register(lkModel)
class lkModelAdmin(admin.ModelAdmin):
    list_display=('id','title','request_url')
    

@admin.register(lkModelType)
class lkModelTypeAdmin(admin.ModelAdmin):
    list_display=('id','model_type')
