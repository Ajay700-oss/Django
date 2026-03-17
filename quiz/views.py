import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Score, GameSettings


def home(request):
    """Landing page – clears any existing session quiz state."""
    request.session.flush()
    settings = GameSettings.load()
    total_questions = Question.objects.count()
    return render(request, 'quiz/home.html', {
        'total_questions': total_questions,
        'timer_seconds': settings.timer_seconds,
        'points_per_question': settings.points_per_question,
    })


def quiz_view(request):
    """Main quiz page – picks a random question the user hasn't seen this session."""
    difficulty = request.GET.get('difficulty', request.session.get('difficulty', 'All'))
    player_name = request.GET.get('player', request.session.get('player_name', 'Player'))

    # Persist in session
    request.session['difficulty'] = difficulty
    request.session['player_name'] = player_name

    # Initialise session counters if needed
    if 'score' not in request.session:
        request.session['score'] = 0
    if 'streak' not in request.session:
        request.session['streak'] = 0
    if 'seen_ids' not in request.session:
        request.session['seen_ids'] = []

    # Filter questions
    qs = Question.objects.all()
    if difficulty != 'All':
        qs = qs.filter(difficulty=difficulty)

    # Exclude already-seen questions
    seen = request.session.get('seen_ids', [])
    remaining = qs.exclude(id__in=seen)

    if not remaining.exists():
        # All questions answered → go to results
        return redirect('quiz:results')

    question = random.choice(list(remaining))

    # Track seen
    seen.append(question.id)
    request.session['seen_ids'] = seen
    request.session.modified = True

    total = qs.count()
    answered = len(seen)
    settings = GameSettings.load()

    context = {
        'question': question,
        'score': request.session['score'],
        'streak': request.session['streak'],
        'difficulty': difficulty,
        'player_name': player_name,
        'answered': answered,
        'total': total,
        'progress_pct': int((answered / total) * 100) if total else 0,
        'timer_seconds': settings.timer_seconds,
        'points_per_question': settings.points_per_question,
    }
    return render(request, 'quiz/quiz.html', context)


@require_POST
def submit_answer(request):
    """AJAX endpoint – checks the answer and updates session state."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    question_id = data.get('question_id')
    selected = data.get('selected', '').upper()

    question = get_object_or_404(Question, pk=question_id)
    correct = question.correct_answer.upper()
    is_correct = selected == correct

    # Update session
    settings = GameSettings.load()
    if is_correct:
        request.session['score'] = request.session.get('score', 0) + settings.points_per_question
        request.session['streak'] = request.session.get('streak', 0) + 1
    else:
        request.session['streak'] = 0
    request.session.modified = True

    options = {
        'A': question.option_a,
        'B': question.option_b,
        'C': question.option_c,
        'D': question.option_d,
    }

    return JsonResponse({
        'correct': is_correct,
        'correct_answer': correct,
        'correct_text': options[correct],
        'explanation': question.explanation,
        'score': request.session['score'],
        'streak': request.session['streak'],
    })


def results_view(request):
    """Results page – saves score to leaderboard and shows summary."""
    score = request.session.get('score', 0)
    streak = request.session.get('streak', 0)
    player_name = request.session.get('player_name', 'Player')
    difficulty = request.session.get('difficulty', 'All')
    total_answered = len(request.session.get('seen_ids', []))

    # Save to leaderboard
    if score > 0:
        Score.objects.create(
            player_name=player_name,
            score=score,
            streak=streak,
            difficulty=difficulty,
        )

    context = {
        'score': score,
        'streak': streak,
        'player_name': player_name,
        'total_answered': total_answered,
        'difficulty': difficulty,
    }
    # Clear session so a new game starts fresh
    request.session.flush()
    return render(request, 'quiz/results.html', context)


def leaderboard_view(request):
    """Top 10 scores."""
    scores = Score.objects.all()[:10]
    return render(request, 'quiz/leaderboard.html', {'scores': scores})
