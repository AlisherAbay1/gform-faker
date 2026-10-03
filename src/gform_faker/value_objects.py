from dataclasses import dataclass
from gform_faker.enums import QuestionEnum

@dataclass
class Question:
    id: str
    text: str
    type: QuestionEnum