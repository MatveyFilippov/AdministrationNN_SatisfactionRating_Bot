from ..base import get_bot_info
from ..global_tools import send_message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State
import random
import string
from typing import NamedTuple


__USED_STRINGS = {None}
def get_free_random_str() -> str:
    result = None
    while result in __USED_STRINGS:
        result = "".join((random.choice(string.printable) for _ in range(12)))
    __USED_STRINGS.add(result)
    return result


FREE_ANSWER = "Другое"


class Question:
    STATES: list[State] = []
    __OBJ_BY_STATE: dict[str, 'Question'] = {}

    def __init__(self, question: str, question_number: int, options: dict[str, 'Question']):
        self.__STATE = State(state=get_free_random_str(), group_name="SurveyQuestion")

        self.__QUESTION = question
        self.__QUESTION_NUMBER = question_number
        self.__OPTIONS = options

        self.__KB = (
            ReplyKeyboardRemove()
            if len(options) == 1 and list(options.keys())[0] == FREE_ANSWER else
            ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(answer)] for answer in options.keys()],
                resize_keyboard=True, one_time_keyboard=True,
            )
        )

        self.__OBJ_BY_STATE[self.__STATE.state] = self
        self.STATES.append(self.__STATE)

    @property
    def question(self) -> str:
        return self.__QUESTION

    @property
    def question_number(self) -> int:
        return self.__QUESTION_NUMBER

    async def send(self, chat_id: int):
        await self.__STATE.set()
        await send_message(chat_id=chat_id, text=self.__QUESTION, kb=self.__KB)

    def for_answer(self, answer: str) -> 'Question':
        if answer in self.__OPTIONS:
            return self.__OPTIONS[answer]
        elif FREE_ANSWER in self.__OPTIONS:
            return self.__OPTIONS[FREE_ANSWER]
        else:
            raise ValueError("No such available answer")

    @classmethod
    def for_state(cls, state: str) -> 'Question':
        return cls.__OBJ_BY_STATE[state]


class Surveys(NamedTuple):
    name: str
    survey_id: int
    first_question: Question

    __SURVEYS = {}

    @property
    async def link_to_start(self) -> str:
        username = (await get_bot_info()).username
        return f"https://t.me/{username}?start={self.survey_id}"

    @classmethod
    def register(cls, name: str, survey_id: int, first_question: Question):
        cls.__SURVEYS[survey_id] = cls(
            name=name,
            survey_id=survey_id,
            first_question=first_question,
        )

    @classmethod
    def get(cls, survey_id: int) -> 'Surveys':
        return cls.__SURVEYS[survey_id]

    @classmethod
    def get_all(cls) -> list['Surveys']:
        return list(cls.__SURVEYS.values())
