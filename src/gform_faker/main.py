import bs4
import requests
import logging
from gform_faker.errors import (
    TorNotConnectedError, UnableToGetFbzxError, UnableToParseFbzxError, 
    UnableToParseFbPublicLoadDataError, UndefinedQuestionTypeError)
import re
import json
from gform_faker.value_objects import Question
from gform_faker.enums import QuestionEnum

def is_tor_active(proxies: dict[str, str]):
    try:
        result = requests.get("https://ident.me", proxies=proxies, timeout=20)
        logging.info(f"Connected to ip {result.text}.")
        return True
    except Exception as e:
        logging.error(f"Unable to connect: [{type(e).__name__}]: {e}")
        return False

def get_fbzx(parsed_data: bs4.BeautifulSoup):
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

def get_form_questions(data: requests.Response):
    answers_match = re.search(r"var FB_PUBLIC_LOAD_DATA_ = (.*?);", data.text)
    if answers_match is None:
        raise UnableToParseFbPublicLoadDataError()
    json_answers = answers_match.group(1)
    raw_answers = json.loads(json_answers)

    form_questions: list[Question] = []

    for raw_question in raw_answers[1][1]:
        try: 
            question_type = raw_question[3]
        except ValueError as e:
            logging.error(f"Undefinded question type accured: {e}")
            raise UndefinedQuestionTypeError()

        if question_type in (QuestionEnum.INFO_TEXT, QuestionEnum.SECTION_HEADER, QuestionEnum.IMAGE):
            continue

        question_id = raw_question[4][0][0]
        question_text = raw_question[1]
        
        question = Question(
            id=question_id, 
            text=question_text, 
            type=QuestionEnum(question_type)
        )
        form_questions.append(question)
    
    return form_questions


def main():
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdyYxnBTs89oL7wyb3aun1P1uLRlfEVZo9jhWoke-AmnbtnlQ/viewform"
    
    proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    }

    if not is_tor_active(proxies):
        raise TorNotConnectedError()

    logging.info("Form parsing started.")
    data = requests.get(url=url, proxies=proxies, timeout=10)
    parsed_data = bs4.BeautifulSoup(data.text, "lxml")
    fbzx = get_fbzx(parsed_data)
    for i in get_form_questions(data):
        print(i)

    
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
