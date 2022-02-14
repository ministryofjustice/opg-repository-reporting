from __future__ import annotations
import pathlib
import json
import glob
import os
from jsonschema import validate, ValidationError
from ..shared import root_directory


class Schema:
    """ Handle the loading and validation of data against schema """

    @staticmethod
    def versions() -> dict:
        """ Return a tulple of lists - first being all version ids, second being their files paths """
        base:pathlib.Path = root_directory().joinpath("./schema/").resolve()
        versions:dict = {}
        file:pathlib.Path       
        for file in glob.glob(f"{base}/*.json"):
            # little unsafe, what if doesnt have a / ?
            key:str = os.path.basename(file).replace('.json', '')            
            versions.update({key: file})
        return versions
       

    @staticmethod
    def default_version():
        """Return the last version """
        return list(Schema.versions().keys()).pop()

    @staticmethod
    def get(version:str) -> dict | None:
        """ Use the version number passed to find and return the schema data """
        schema:dict = None
        versions:dict = Schema.versions()
        # get the matching version, or the first
        path:pathlib.Path = versions.get(version, None)
        # read the file
        if path is not None:
            file = open(path, 'r', encoding='utf-8')
            schema = json.load(file)
            file.close()
        return schema


    @staticmethod
    def valid(metadata:dict):
        """Determine if the metadata passed in validates against a version of the schema """
        schema_url:str = metadata.get("$schema", Schema.default_version())
        # clean out any url / file structures
        version = schema_url[schema_url.rfind('/')+1:].replace('.json', '') if schema_url.rfind('/') > 0 else schema_url.replace('.json', '')
        # get the dict
        schema:dict = Schema.get(version)
        try:
            validate(instance=metadata, schema=schema)
            return True
        except ValidationError:
            pass
        return False
