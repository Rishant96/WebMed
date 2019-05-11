from django.contrib import admin
from .models import Emergency, Emergency_Group
from .models import Condition, Variety

admin.site.register(Emergency)
admin.site.register(Emergency_Group)


class VarietyInline(admin.StackedInline):
    model = Variety


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    inlines = [
        VarietyInline,
    ]
