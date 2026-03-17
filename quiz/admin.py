from django.contrib import admin
from .models import Question, Score, GameSettings


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_snippet', 'difficulty', 'correct_answer')
    list_filter = ('difficulty',)
    search_fields = ('code_snippet',)

    def short_snippet(self, obj):
        return obj.code_snippet[:80]
    short_snippet.short_description = 'Code Snippet'


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'score', 'streak', 'difficulty', 'created_at')
    list_filter = ('difficulty',)
    ordering = ('-score',)


@admin.register(GameSettings)
class GameSettingsAdmin(admin.ModelAdmin):
    list_display = ('timer_seconds', 'points_per_question')

    def has_add_permission(self, request):
        # Only allow one row
        return not GameSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
