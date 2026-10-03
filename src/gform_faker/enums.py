from enum import IntEnum

# 6, 8, 11 are not interactive elements. 

class QuestionEnum(IntEnum):
    SHORT_TEXT = 0
    PARAGRAPH = 1
    RADIO = 2
    DROPDOWN = 3
    CHECKBOX = 4
    SCALE = 5
    INFO_TEXT = 6
    GRID = 7
    SECTION_HEADER = 8
    DATE = 9
    TIME = 10
    IMAGE = 11
    FIGURED_SCALE = 18