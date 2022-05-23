
from . import ServiceBase
from . import ApiCaller



class ServiceEc2(ServiceBase):
    """Handle ec2 related resource calls"""

    client_type: str = 'ec2'
    _find:dict = {
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
        'reserved_instances': ApiCaller('describe_reserved_instances', 'ReservedInstances', 'ReservedInstancesId'),
        'route_tables': ApiCaller('describe_route_tables', 'RouteTables', 'RouteTableId'),
        'security_groups': ApiCaller('describe_security_groups', 'SecurityGroups', 'GroupId'),
        'subnets': ApiCaller('describe_subnets', 'Subnets', 'SubnetId'),
        'transit_gateways': ApiCaller('describe_transit_gateways', 'TransitGateways', 'TransitGatewayId'),
        'volumes': ApiCaller('describe_volumes', 'Volumes', 'VolumeId'),
        'vpcs': ApiCaller('describe_vpcs', 'Vpcs', 'VpcId'),
    }
    _kwargs:dict = {
        'images': {'Owners': ['self']}
    }
    _tag_names:dict = {
        'network_interfaces': 'TagSet'
    }
    
    

    