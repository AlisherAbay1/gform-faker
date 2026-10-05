from dataclasses import dataclass
from gform_faker.enums import QuestionEnum

@dataclass
class Entry:
    id: str
    answer_options: list[str] | None
    row_label: str | None = None


@dataclass
class Question: 
    text: str | None
    type: QuestionEnum
    answer_required: bool
    entries: list[Entry]


@dataclass
class GridQuestion(Question):
    multi: bool = False