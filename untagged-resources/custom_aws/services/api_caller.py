
from pprintpp import pprint


class ApiCaller:
    """Helper to make api calls"""

    client: None
    method: str
    result_key: str
    id_key:str

    def __init__(self, method:str, result_key:str, id_key:str) -> None:
        self.method = method    
        self.result_key = result_key
        self.id_key = id_key
        

    async def call(self, client, **kwargs) -> list:
        """Magic method to handle all the list|describe types calls"""
        call_method = getattr(client, self.method)
        pprint(f"[{self.method}]")
        result:dict = dict (await call_method(**kwargs))
        if '.' in self.result_key:
            found = []
            for key in self.result_key.split('.'):
                found = result.get(key, [])
            return found

        return result.get(self.result_key, [])