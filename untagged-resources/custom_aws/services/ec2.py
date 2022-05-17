import aioboto3
from pprintpp import pprint
from . import ServiceBase


class ServiceEc2(ServiceBase):
    """Handle ec2 related resource calls"""

    client_type: str = 'ec2'

    async def describe_network_interfaces(self, region_name:str) -> list:
        """Find all network instances"""
        untagged = []
        
        session = aioboto3.Session(region_name=region_name)
        async with session.client(self.client_type, region_name=region_name) as client:
            results = await client.describe_network_interfaces()
            #pprint(results)
            

        return untagged

    async def all(self, region_name:str) -> list:
        """Return all the arns of all resources in the ec2 scope that don't contain tags"""
        arns = []
        network_instances = await self.describe_network_interfaces(region_name)

        return arns

    