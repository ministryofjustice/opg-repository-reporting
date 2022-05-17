import aioboto3
from pprintpp import pprint
from . import ServiceBase
from . import ApiCaller



class ServiceEc2(ServiceBase):
    """Handle ec2 related resource calls"""

    client_type: str = 'ec2'
    _describe:dict = {
        'addresses': ApiCaller('describe_addresses', 'Addresses', 'AllocationId'),
        'flow_logs': ApiCaller('describe_flow_logs', 'FlowLogs', 'ResourceId'),
        'hosts': ApiCaller('describe_hosts', 'Hosts', 'HostId'),
        'images': ApiCaller('describe_images', 'Images', 'ImageId'),
        'instances': ApiCaller('describe_instances', 'Reservations.Instances', 'InstanceId'),
        'internet_gateways': ApiCaller('describe_internet_gateways', 'InternetGateways', 'InternetGatewayId'),
        'key_pairs': ApiCaller('describe_key_pairs', 'KeyPairs', 'KeyPairId'),
        'local_gateways': ApiCaller('describe_local_gateways', 'LocalGateways', 'LocalGatewayId'),
        'nat_gateways': ApiCaller('describe_nat_gateways', 'NatGateways', 'NatGatewayId'),
        'network_acls': ApiCaller('describe_network_acls', 'NetworkAcls', 'NetworkAclId'),
        'network_interfaces': ApiCaller('describe_network_interfaces', 'NetworkInterfaces', 'NetworkInterfaceId'),        
    }
    _kwargs:dict = {
        'images': {'Owners': ['self']}
    }
    _tags:dict = {
        'network_interfaces': 'TagSet'
    }
    
    async def all(self, region_name:str) -> dict:
        """Return all the arns of all resources in the ec2 scope that don't contain tags"""
        untagged = []
        session = aioboto3.Session(region_name=region_name)

        async with session.client(self.client_type, region_name=region_name) as client:
            for key, instance in self._describe.items():
                kwargs = self._kwargs.get(key, None)
                if kwargs is not None:
                    result = await instance.call(client, **kwargs)
                else:
                    result = await instance.call(client)
                # merge those in
                self.arns.extend(
                    [d.get(instance.id_key, []) for d in result]
                )
                tag_field = self._tags.get(key, None)
                if tag_field is not None:
                    untagged.extend( self._untagged(result, instance.id_key, tag_field))
                else:
                    untagged.extend( self._untagged(result, instance.id_key))
                    
        pprint(untagged)
        return {'untagged': untagged, 'all': self.arns}

    