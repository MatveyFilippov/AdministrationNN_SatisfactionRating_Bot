import sspd
from enum import Enum, auto
from typing import NoReturn
import os


class Direction(Enum):
    EXIT = 0
    UPDATE_CODE = auto()
    DOWNLOAD_LOG_FILE = auto()
    DOWNLOAD_DATABASE_FILE = auto()
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


def download_database_file():
    remote_db_file_path = sspd.base.tilda_replacer(sspd.base.config.get_required_value(
        section="RemoteMachine", option="REMOTE_DB_FILE_PATH"
    ))
    local_db_file_path_to_download_in = sspd.base.config.get_required_value(
        section="LocalMachine", option="LOCAL_DB_FILE_PATH_TO_DOWNLOAD_IN"
    )

    if not os.path.exists(local_db_file_path_to_download_in):
        os.makedirs(os.path.dirname(local_db_file_path_to_download_in), exist_ok=True)
    else:
        print(f"File '{local_db_file_path_to_download_in}' already exists")
        sign2continue = "Y"
        if input(f"Can I rewrite it ({sign2continue}/n): ").strip() != sign2continue:
            return

    sspd.tasks.download_file_from_remote_server(
        remote_filepath=remote_db_file_path, local_filepath=local_db_file_path_to_download_in
    )


HANDLERS = {
    Direction.EXIT: lambda: None,
    Direction.UPDATE_CODE: sspd.tasks.update_remote_code,
    Direction.START_RUNNING: sspd.tasks.start_running_remote_code,
    Direction.STOP_RUNNING: sspd.tasks.stop_running_remote_code,
    Direction.DOWNLOAD_LOG_FILE: sspd.tasks.download_log_file,
    Direction.DOWNLOAD_DATABASE_FILE: download_database_file,
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
