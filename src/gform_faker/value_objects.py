from dataclasses import dataclass
from gform_faker.enums import ElementEnum

@dataclass
class Entry:
    id: str
    answer_options: list[str] | None
    row_label: str | None = None


@dataclass
class Question: 
    text: str | None
    type: ElementEnum
    answer_required: bool
    entries: list[Entry]


@dataclass
class StaticItem:
    text: str
    type: ElementEnum


@dataclass
class GridQuestion(Question):
    multi: bool = False