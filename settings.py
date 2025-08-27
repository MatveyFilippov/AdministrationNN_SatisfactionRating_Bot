import json
import logging
from typing import Final, Type
from zoneinfo import ZoneInfo


class SettingsJSON:
    SETTINGS_FILEPATH = "BotSettings.json"

    @classmethod
    def __get_dict_from_json_file(cls) -> dict:
        result = dict()
        try:
            with open(cls.SETTINGS_FILEPATH, "r", encoding="UTF-8") as jf:
                result = dict(json.load(jf))
        except FileNotFoundError:
            with open(cls.SETTINGS_FILEPATH, "w", encoding="UTF-8") as jf:
                json.dump(result, jf, ensure_ascii=False)
        return result

    @classmethod
    def get(cls, var_name: str, required_type: Type | None = str, prompt: str | None = None):
        json_file_dict = cls.__get_dict_from_json_file()
        try:
            return required_type(json_file_dict[var_name])
        except (KeyError, TypeError):
            if not prompt:
                prompt = f"{var_name}: "
            return cls.__ask_and_append(var_name=var_name, prompt=prompt, required_type=required_type)

    @classmethod
    def get_optional(cls, var_name: str, default=None, write_default=True):
        json_file_dict = cls.__get_dict_from_json_file()
        try:
            return json_file_dict[var_name]
        except (KeyError, TypeError):
            if default is not None and write_default:
                cls.__append_to_json_file(key=var_name, value=default)
            return default

    @classmethod
    def __ask_value(cls, prompt: str, required_type: Type | None = str):
        while True:
            try:
                return required_type(input(prompt))
            except ValueError:
                print(f" >>> Value should be '{required_type}'")

    @classmethod
    def __append_to_json_file(cls, key: str, value):
        json_file_dict = cls.__get_dict_from_json_file()
        json_file_dict[key] = value
        with open(cls.SETTINGS_FILEPATH, "w", encoding="UTF-8") as jf:
            json.dump(json_file_dict, jf, ensure_ascii=False)

    @classmethod
    def __ask_and_append(cls, var_name: str, prompt: str, required_type: Type | None = str):
        value = cls.__ask_value(prompt=prompt, required_type=required_type)
        cls.__append_to_json_file(key=var_name, value=value)
        return value


BOT_API_TOKEN: Final = SettingsJSON.get(var_name="BOT_API_TOKEN")
BOT_ADMIN_IDs: Final = set(SettingsJSON.get_optional(var_name="BOT_ADMIN_IDs", default=[]))
BOT_TIMEZONE: Final = ZoneInfo(SettingsJSON.get_optional(var_name="BOT_TIMEZONE", default="Europe/Moscow"))
BOT_TIMEZONE_ABBREVIATION: Final = SettingsJSON.get_optional(var_name="BOT_TIMEZONE_ABBREVIATION", default=BOT_TIMEZONE.key, write_default=False)
DATETIME_FORMAT: Final = SettingsJSON.get_optional(var_name="DATETIME_FORMAT", default="%Y-%m-%d %H:%M:%S", write_default=False)
LINK_TO_DATABASE: Final = SettingsJSON.get(var_name="LINK_TO_DATABASE", prompt=(
    "Use:\n * SQLite: '"
    "sqlite:///{path_to_db_file}"
    "'\n * PostgreSQL: '"
    "postgresql+psycopg2://{user}:{password}@{ip}:{port}/{db_name}"
    "'\nWrite link to db: "
))

logging.basicConfig(
    level=logging.INFO, filename=f"AdministrationNN_SatisfactionRating_Bot.log", encoding="UTF-8",
    datefmt=DATETIME_FORMAT, format="\n'%(name)s':\n%(levelname)s %(asctime)s --> %(message)s",
)
logging.getLogger('aiogram').setLevel(logging.ERROR)
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
