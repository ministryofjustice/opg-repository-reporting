class ServiceBase:
    """Base class for AWS service calls"""
    arns: list = []

    def _untagged(self, dataset:list, id_key:str, tag_key:str = 'tags') -> list:
        """Return arn that arent tagged """
        untagged: list = []
        for item in list(dataset): 
            tags = list ( item.get(tag_key, []) )
            if len(tags) == 0:
                untagged.append(item.get(id_key, None))
        return untagged



    async def all(self, region_name:str) -> dict:
        """Return a list of all data from this service"""

        return {}