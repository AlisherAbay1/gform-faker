from gform_faker.value_objects import Entry
from gform_faker.enums import ElementEnum
from collections.abc import Mapping, Callable

def get_parsers():
    return {
        ElementEnum.SHORT_TEXT: create_entry_without_options,
        ElementEnum.PARAGRAPH: create_entry_without_options,
        ElementEnum.DATE: create_entry_without_options,
        ElementEnum.TIME: create_entry_without_options,
        ElementEnum.RADIO: create_one_entry,
        ElementEnum.DROPDOWN: create_one_entry,
        ElementEnum.CHECKBOX: create_one_entry,
        ElementEnum.SCALE: create_one_entry,
        ElementEnum.FIGURED_SCALE: create_one_entry,
        ElementEnum.GRID: create_table_entries,
    }

def get_answer_options(raw_entry: list):
    return [answer_option[0] for answer_option in raw_entry[1]]

def create_entry_without_options(raw_question: list):
    return [Entry(
        id=raw_question[4][0][0], 
        answer_options=None)]

def create_one_entry(raw_question: list):
    return [Entry(
        id=raw_question[4][0][0], 
        answer_options=get_answer_options(raw_question[4][0]))]

def create_table_entries(raw_question: list):
    entries = []
    for raw_entry in raw_question[4]:
        entries.append(Entry(
            id=raw_entry[0], 
            answer_options=get_answer_options(raw_entry), 
            row_label=raw_entry[3][0]
        ))
    return entries

def create_entry(raw_question: list, question_type: ElementEnum, parsers: Mapping[ElementEnum, Callable]):
    return parsers[question_type](raw_question)