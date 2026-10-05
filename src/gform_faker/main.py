import bs4
import requests
import logging
from gform_faker.errors import (
    TorNotConnectedError, UnableToGetFbzxError, UnableToParseFbzxError, 
    UnableToParseFbPublicLoadDataError, UndefinedQuestionTypeError)
import re
import json
from gform_faker.value_objects import Question, Entry, StaticItem
from gform_faker.enums import ElementEnum
from gform_faker.entry_functions import get_parsers, create_entry
from collections.abc import Mapping, Callable

def is_tor_active(proxies: dict[str, str]):
    try:
        result = requests.get("https://ident.me", proxies=proxies, timeout=20)
        logging.info(f"Connected to ip {result.text}.")
        return True
    except Exception as e:
        logging.error(f"Unable to connect: [{type(e).__name__}]: {e}")
        return False

def get_fbzx_token(parsed_data: bs4.BeautifulSoup):
    raw_fbzx = parsed_data.find("input", attrs={"name": "fbzx"})
    if raw_fbzx:
        parsed_fbzx = raw_fbzx.get("value")
        if parsed_fbzx is None:
            logging.error("Parsed fbzx value is None for some reason.")
            raise UnableToParseFbzxError()
        logging.info(f"Fbzx value: {parsed_fbzx}")
        return parsed_fbzx
    else:
        logging.error(f"For {raw_fbzx} is impossible to parse fbzx.")
        raise UnableToGetFbzxError()

def get_form_elements(data: requests.Response, parsers: Mapping[ElementEnum, Callable]):
    answers_match = re.search(r"var FB_PUBLIC_LOAD_DATA_ = (.*?);", data.text)
    if answers_match is None:
        raise UnableToParseFbPublicLoadDataError()
    json_answers = answers_match.group(1)
    raw_answers = json.loads(json_answers)

    form_elements: list[Question | StaticItem] = []

    for raw_element in raw_answers[1][1]:
        try: 
            element_type = raw_element[3]
        except ValueError as e:
            logging.error(f"Undefinded question type accured: {e}")
            raise UndefinedQuestionTypeError()

        element_text = raw_element[1]

        if element_type in (ElementEnum.INFO_TEXT, ElementEnum.SECTION_HEADER, ElementEnum.IMAGE):
            form_elements.append(
                StaticItem(
                    text=element_text, 
                    type=ElementEnum(element_type)
                )
            )
            continue
        
        answer_required = bool(raw_element[4][0][2])
        entries: list[Entry] = create_entry(raw_element, element_type, parsers)

        question = Question(
            text=element_text, 
            type=ElementEnum(element_type), 
            answer_required=answer_required, 
            entries=entries
        )
        form_elements.append(question)
    
    return form_elements


def main():
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdyYxnBTs89oL7wyb3aun1P1uLRlfEVZo9jhWoke-AmnbtnlQ/viewform"
    
    proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    }

    parsers = get_parsers()

    if not is_tor_active(proxies):
        raise TorNotConnectedError()

    logging.info("Form parsing started.")
    data = requests.get(url=url, proxies=proxies, timeout=10)
    parsed_data = bs4.BeautifulSoup(data.text, "lxml")
    fbzx_token = get_fbzx_token(parsed_data)
    elements = get_form_elements(data, parsers)
    section_headers_count = sum([1 for element in elements if element.type == ElementEnum.SECTION_HEADER])
    page_history = ",".join([str(page) for page in range(section_headers_count + 1)])
    payload = {'fvv': '1', 'pageHistory': page_history, 'fbzx': fbzx_token}
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
