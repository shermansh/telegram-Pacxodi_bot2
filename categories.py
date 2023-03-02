"""Работа с категориями расходов"""
from typing import Dict, List, NamedTuple

import db

"""Структура категории"""

class Category(NamedTuple):
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    """Возвращает справочник категорий расходов из БД"""

    def _load_categories(self) -> List[Category]:
        categories = db.fetchall(
            "category", "codename name is_base_expense aliases".split()
        )
        categories = self._fill_aliases(categories)
        return categories

    """Заполняет по каждой категории aliases, то есть возможные
            названия этой категории, которые можем писать в тексте сообщения.
            Например, категория «кафе» может быть написана как cafe,
            ресторан и тд."""

    def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                is_base_expense=category['is_base_expense'],
                aliases=aliases
            ))
        return categories_result

    """Возвращает справочник категорий."""

    def get_all_categories(self) -> List[Dict]:
        return self._categories

    def get_category(self, category_name: str) -> Category:
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded
