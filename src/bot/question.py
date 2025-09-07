import tomllib
import random

from src.bot.config import settings

def get_question_from_category(category_key: str) -> str:
    with open(settings.questions_file, "rb") as f:
        data = tomllib.load(f)
        print(data)

    category = data.get(category_key)

    if not category:
        raise ValueError(f"Категория не найдена.")

    questions = category.get("questions")
    if not questions:
        raise ValueError(f"В этой категории нет вопросов.")

    return random.choice(questions)
