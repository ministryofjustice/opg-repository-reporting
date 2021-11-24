from datetime import datetime

class out:
    """
    Static helper class to handle action output
    """

    @staticmethod
    def ts():
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def debug(message:str):
        print(f"::debug::({out.ts()}) {message}")

    @staticmethod
    def log(message:str):
        print(f"({out.ts()}) {message}")

    @staticmethod
    def notice(message:str, title:str = "", file:str = "", line:str = "", endLine:str = ""):
        print(f"::notice file={file},line={line},endLine={endLine},title={title}::({out.ts()}) {message}")

    @staticmethod
    def warning(message:str, title:str = "", file:str = "", line:str = "", endLine:str = ""):
        print(f"::warning file={file},line={line},endLine={endLine},title={title}::({out.ts()}) {message}")

    @staticmethod
    def error(message:str, title:str = "", file:str = "", line:str = "", endLine:str = ""):
        print(f"::error file={file},line={line},endLine={endLine},title={title}::({out.ts()}) {message}")

    @staticmethod
    def group_start(title:str):
        print(f"::group::{title}")

    @staticmethod
    def group_end():
        print(f"::endgroup::")

    @staticmethod
    def set_var(name, value):
        print(f"::set-output name={name}::{value}")
