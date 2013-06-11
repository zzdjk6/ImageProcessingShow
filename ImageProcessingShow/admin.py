from django.contrib import admin
from ImageProcessingShow.models import Operation

class OperationAdmin(admin.ModelAdmin):
    list_display = ['name','label','url']

admin.site.register(Operation, OperationAdmin)