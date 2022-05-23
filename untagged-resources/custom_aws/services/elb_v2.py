from pydoc import cli
import aioboto3
from . import ServiceBase

class ServiceElbv2(ServiceBase):
    """Handle elb related resources"""

    client_type:str = 'elbv2'
    

    async def all(self, region_name:str) -> dict:
        """ELB api does not return the tags in the first call, there is a second call per elb to find them"""
        untagged = []
        all_resources = []
        session = aioboto3.Session(region_name=region_name)
        async with session.client(self.client_type, region_name=region_name) as client:
            load_balancers = await client.describe_load_balancers()
            # just get the arns
            load_balancer_arns = [ lb.get('LoadBalancerArn') for lb in load_balancers.get('LoadBalancers', [])]
            # merge
            all_resources.extend(load_balancer_arns)            

            # now get the tags for all the arns
            tag_data = await client.describe_tags(ResourceArns = load_balancer_arns)
            for tag in tag_data.get('TagDescriptions', []):
                tags = tag.get('Tags', [])
                if len(tags) == 0:
                    untagged.append(
                        tag.get('ResourceArn')
                    )
            
            print(f"\t - [describe_load_balancers]\n\t\t All: [{(len(load_balancer_arns))}]\t Untagged: [{len(untagged)}]")

        return {'all':all_resources, 'untagged':untagged}
        
    
    

    