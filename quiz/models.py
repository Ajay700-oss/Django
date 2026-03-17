from django.db import models


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    code_snippet = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Easy')
    explanation = models.TextField(blank=True, help_text="Brief explanation of why the answer is correct.")

    def __str__(self):
        return f"[{self.difficulty}] {self.code_snippet[:60]}..."


class Score(models.Model):
    player_name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=10, default='All')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-streak', '-created_at']

    def __str__(self):
        return f"{self.player_name} — {self.score} pts"


class GameSettings(models.Model):
    """Singleton model — only one row should exist. Editable from Django Admin."""
    timer_seconds = models.PositiveIntegerField(
        default=15,
        help_text="Seconds allowed per question (e.g. 10, 15, 20)."
    )
    points_per_question = models.PositiveIntegerField(
        default=10,
        help_text="Points awarded for each correct answer."
    )

    class Meta:
        verbose_name = "Game Settings"
        verbose_name_plural = "Game Settings"

    def __str__(self):
        return f"Timer: {self.timer_seconds}s | Points: {self.points_per_question}"

    def save(self, *args, **kwargs):
        # Enforce singleton — always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Return the single settings row, creating it with defaults if needed."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
