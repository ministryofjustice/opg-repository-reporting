from datetime import datetime

class Out:
    """
    Static helper class to handle action output
    """

    @staticmethod
    def ts() -> str:
        """ Return string formatted timestamp of now """ 
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def debug(message:str) -> None:
        """Output as debug level details for the githu action"""
        print(f"::debug::({Out.ts()}) {message}")

    @staticmethod
    def log(message:str) -> None:
        """Output as standard log level for github action """
        print(f"({Out.ts()}) {message}")

    @staticmethod
    def notice(message:str, title:str = "", file:str = "", line:str = "", endLine:str = "") -> None:
        """Output as a notice """
        print(f"::notice file={file},line={line},endLine={endLine},title={title}::({Out.ts()}) {message}")

    @staticmethod
    def warning(message:str, title:str = "", file:str = "", line:str = "", endLine:str = "") -> None:
        """Output as a warning"""
        print(f"::warning file={file},line={line},endLine={endLine},title={title}::({Out.ts()}) {message}")

    @staticmethod
    def error(message:str, title:str = "", file:str = "", line:str = "", endLine:str = "") -> None:
        """Output as an error"""
        print(f"::error file={file},line={line},endLine={endLine},title={title}::({Out.ts()}) {message}")

    @staticmethod
    def group_start(title:str) -> None:
        """Create a output group"""
        print(f"::group::{title}")

    @staticmethod
    def group_end() -> None:
        """End an output group"""
        print("::endgroup::")

    @staticmethod
    def set_var(name, value) -> None:
        """Set a github action variable value"""
        print(f"::set-output name={name}::{value}")
