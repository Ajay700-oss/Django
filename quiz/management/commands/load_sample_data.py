"""
Management command to populate the database with sample Python quiz questions.
Usage:  python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from quiz.models import Question


SAMPLE_QUESTIONS = [
    # ─── Easy ────────────────────────────────
    {
        "code_snippet": 'print(type(3.14).__name__)',
        "option_a": "int",
        "option_b": "float",
        "option_c": "double",
        "option_d": "number",
        "correct_answer": "B",
        "difficulty": "Easy",
        "explanation": "3.14 is a floating-point literal, so type() returns <class 'float'> and __name__ gives 'float'.",
    },
    {
        "code_snippet": "x = [1, 2, 3]\nprint(len(x))",
        "option_a": "2",
        "option_b": "4",
        "option_c": "3",
        "option_d": "Error",
        "correct_answer": "C",
        "difficulty": "Easy",
        "explanation": "len() returns the number of elements in the list, which is 3.",
    },
    {
        "code_snippet": 'print("hello"[1])',
        "option_a": "h",
        "option_b": "e",
        "option_c": "l",
        "option_d": "o",
        "correct_answer": "B",
        "difficulty": "Easy",
        "explanation": "Python strings are 0-indexed. Index 1 is the character 'e'.",
    },
    {
        "code_snippet": "print(10 // 3)",
        "option_a": "3.33",
        "option_b": "3",
        "option_c": "4",
        "option_d": "3.0",
        "correct_answer": "B",
        "difficulty": "Easy",
        "explanation": "// is floor division and both operands are ints, so the result is int 3.",
    },
    {
        "code_snippet": "x = True\nprint(x + 2)",
        "option_a": "True2",
        "option_b": "Error",
        "option_c": "3",
        "option_d": "12",
        "correct_answer": "C",
        "difficulty": "Easy",
        "explanation": "In Python, True is treated as 1 in arithmetic, so 1 + 2 = 3.",
    },
    # ─── Medium ──────────────────────────────
    {
        "code_snippet": "a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)",
        "option_a": "[1, 2, 3]",
        "option_b": "[1, 2, 3, 4]",
        "option_c": "[4, 1, 2, 3]",
        "option_d": "Error",
        "correct_answer": "B",
        "difficulty": "Medium",
        "explanation": "b = a creates a reference, not a copy. Both point to the same list.",
    },
    {
        "code_snippet": 'print("abc" * 2 + "d")',
        "option_a": "abcabcd",
        "option_b": "abc2d",
        "option_c": "aabbccd",
        "option_d": "Error",
        "correct_answer": "A",
        "difficulty": "Medium",
        "explanation": "String * 2 repeats it, then + concatenates: 'abcabc' + 'd' = 'abcabcd'.",
    },
    {
        "code_snippet": "x = {1, 2, 3}\ny = {3, 4, 5}\nprint(x & y)",
        "option_a": "{1, 2, 3, 4, 5}",
        "option_b": "{3}",
        "option_c": "{1, 2}",
        "option_d": "Error",
        "correct_answer": "B",
        "difficulty": "Medium",
        "explanation": "& is the set intersection operator, returning elements common to both sets.",
    },
    {
        "code_snippet": "def f(x, lst=[]):\n    lst.append(x)\n    return lst\n\nprint(f(1))\nprint(f(2))",
        "option_a": "[1]\\n[2]",
        "option_b": "[1]\\n[1, 2]",
        "option_c": "Error",
        "option_d": "[1, 2]\\n[1, 2]",
        "correct_answer": "B",
        "difficulty": "Medium",
        "explanation": "Default mutable arguments persist across calls. The list accumulates values.",
    },
    {
        "code_snippet": "print(bool(\"\"), bool(\" \"))",
        "option_a": "False False",
        "option_b": "True True",
        "option_c": "False True",
        "option_d": "True False",
        "correct_answer": "C",
        "difficulty": "Medium",
        "explanation": 'An empty string is falsy, but a string with a space is truthy (non-empty).',
    },
    # ─── Hard ────────────────────────────────
    {
        "code_snippet": "x = [1, 2, 3]\ny = x[:]\ny[0] = 99\nprint(x[0])",
        "option_a": "99",
        "option_b": "1",
        "option_c": "[99, 2, 3]",
        "option_d": "Error",
        "correct_answer": "B",
        "difficulty": "Hard",
        "explanation": "x[:] creates a shallow copy. Changing y does not affect x for immutable elements.",
    },
    {
        "code_snippet": "print([i**2 for i in range(5) if i % 2 == 0])",
        "option_a": "[0, 4, 16]",
        "option_b": "[1, 9, 25]",
        "option_c": "[0, 2, 4]",
        "option_d": "[4, 16]",
        "correct_answer": "A",
        "difficulty": "Hard",
        "explanation": "Even numbers in range(5) are 0,2,4. Their squares are 0, 4, 16.",
    },
    {
        "code_snippet": "def outer():\n    x = 'outer'\n    def inner():\n        nonlocal x\n        x = 'inner'\n    inner()\n    print(x)\n\nouter()",
        "option_a": "outer",
        "option_b": "inner",
        "option_c": "Error",
        "option_d": "None",
        "correct_answer": "B",
        "difficulty": "Hard",
        "explanation": "nonlocal allows inner() to modify the enclosing scope's x, changing it to 'inner'.",
    },
    {
        "code_snippet": "a = (1, 2, [3, 4])\na[2].append(5)\nprint(a)",
        "option_a": "Error",
        "option_b": "(1, 2, [3, 4])",
        "option_c": "(1, 2, [3, 4, 5])",
        "option_d": "(1, 2, 3, 4, 5)",
        "correct_answer": "C",
        "difficulty": "Hard",
        "explanation": "Tuples are immutable, but the list inside is mutable. We can modify it in-place.",
    },
    {
        "code_snippet": "g = (x for x in range(3))\nprint(type(g).__name__)",
        "option_a": "list",
        "option_b": "tuple",
        "option_c": "generator",
        "option_d": "range",
        "correct_answer": "C",
        "difficulty": "Hard",
        "explanation": "Parentheses with a comprehension syntax create a generator object.",
    },
]


class Command(BaseCommand):
    help = "Load sample Python quiz questions into the database."

    def handle(self, *args, **options):
        created = 0
        for q in SAMPLE_QUESTIONS:
            obj, was_created = Question.objects.get_or_create(
                code_snippet=q["code_snippet"],
                defaults=q,
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done! {created} new question(s) added ({Question.objects.count()} total)."
        ))
