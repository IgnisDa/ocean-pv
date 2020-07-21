from django.contrib import admin
from interactions.models import (
    SelfAnswerGroup,
    RelationAnswerGroup,
    GlobalAverages
)


admin.site.site_header = 'ocean-pv administration'


@admin.register(SelfAnswerGroup)
class SelfAnswerGroupAdmin(admin.ModelAdmin):
    readonly_fields = ['return_formatted_json', 'scores', 'accuracy']
    fieldsets = [
        ('User Information', {
            'fields': ['self_user_profile']
        }),
        ('Answer and questions', {
            'fields': ['accuracy', 'scores', 'return_formatted_json']
        })
    ]


@admin.register(RelationAnswerGroup)
class RelationAnswerGroupAdmin(admin.ModelAdmin):
    readonly_fields = ['scores', 'accuracy', 'return_formatted_json']


@admin.register(GlobalAverages)
class GlobalAveragesAdmin(admin.ModelAdmin):
    readonly_fields = ('openness', 'conscientiousness', 'extraversion',
                       'agreeableness', 'neuroticism', 'calculated_on')
