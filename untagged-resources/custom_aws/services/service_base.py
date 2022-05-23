import aioboto3
from pprintpp import pprint

class ServiceBase:
    """Base class for AWS service calls"""
    arns: list = []
    client_type:str = ""

    _find:dict = {}
    _kwargs:dict = {}
    _tag_names:dict = {}



    def _untagged(self, dataset:list, id_key:str, tag_key:str = 'tags', prefix:str = "") -> list:
        """Return arn that arent tagged """
        untagged: list = []
        for item in list(dataset): 
            tags = list ( item.get(tag_key, []) )
            if len(tags) == 0:
                untagged.append(
                    f"{prefix}{item.get(id_key, None)}"
                )
        return untagged



    async def all(self, region_name:str) -> dict:
        """Return all the arns of all resources in the client_type scope that don't contain tags"""
        untagged = []
        session = aioboto3.Session(region_name=region_name)

        async with session.client(self.client_type, region_name=region_name) as client:
            for key, instance in self._find.items():
                prefix:str = f"{self.client_type}/{key}/"

                kwargs = self._kwargs.get(key, None)
                # check if we need to pass extra params
                if kwargs is not None:
                    result = await instance.call(client, **kwargs)
                else:
                    result = await instance.call(client)
                # merge those in
                self.arns.extend(
                    [d.get(instance.id_key, []) for d in result]
                )
                # check if this uses a different name for tags
                tag_field = self._tag_names.get(key, None)
                if tag_field is not None:
                    untagged.extend( self._untagged(result, instance.id_key, tag_field, prefix=prefix))
                else:
                    untagged.extend( self._untagged(result, instance.id_key, prefix=prefix))

        pprint(untagged)
        return {'untagged': untagged, 'all': self.arns}