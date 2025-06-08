import sspd
from enum import Enum, auto
from typing import NoReturn
import os


class Direction(Enum):
    EXIT = 0
    UPDATE_CODE = auto()
    DOWNLOAD_LOGS = auto()
    DOWNLOAD_DATABASE = auto()
    STOP_RUNNING = auto()
    START_RUNNING = auto()

    @classmethod
    def get_direction(cls) -> 'Direction':
        print("Choose what will be done")
        for direction in cls:
            name = direction.name.replace("_", " ").title()
            print(f" * {name} ({direction.value})")
        try:
            return cls(int(input(": ").strip()))
        except ValueError:
            print("No such variant -> exit")
            return cls.EXIT


def download_database():
    sspd.tasks.download_file_from_remote_server(
        remote_filepath=sspd.base.REMOTE_PROJECT_DIR_PATH + "/AdministrationNN_SatisfactionRating_Bot.db",
        local_filepath=os.path.join(sspd.base.LOCAL_PROJECT_DIR_PATH, "AdministrationNN_SatisfactionRating_Bot.db")
    )


HANDLERS = {
    Direction.EXIT: lambda: None,
    Direction.UPDATE_CODE: sspd.tasks.update_remote_code,
    Direction.START_RUNNING: sspd.tasks.start_running_remote_code,
    Direction.STOP_RUNNING: sspd.tasks.stop_running_remote_code,
    Direction.DOWNLOAD_LOGS: sspd.tasks.download_log_file,
    Direction.DOWNLOAD_DATABASE: download_database,
}


def main() -> NoReturn:
    try:
        while True:
            user_decision = Direction.get_direction()
            if user_decision == Direction.EXIT:
                break
            HANDLERS[user_decision]()
            print()
    finally:
        sspd.close_connections()


if __name__ == "__main__":
    main()
