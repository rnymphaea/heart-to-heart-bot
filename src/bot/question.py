import tomllib
import random

from src.bot.config import settings

def get_question_from_category(category_key: str) -> str:
    with open(settings.questions_file, "rb") as f:
        data = tomllib.load(f)

    category = data.get(category_key)

    if not category:
        raise ValueError(f"категория не найдена.")

    questions = category.get("questions")
    if not questions:
        raise ValueError(f"в этой категории нет вопросов.")

    return random.choice(questions)


def get_random_question() -> str:
    with open(settings.questions_file, "rb") as f:
        data = tomllib.load(f)

    all_questions = []
    for category, value in data.items():
        questions = value.get("questions", [])
        all_questions.extend(questions)
    if not all_questions:
        raise ValueError("в базе пока нет вопросов")

    return random.choice(all_questions)
