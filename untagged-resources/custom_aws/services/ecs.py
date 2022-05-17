import aioboto3
from pprintpp import pprint
from . import ServiceBase
from . import ApiCaller

class ServiceEcs(ServiceBase):
    """Handle ecs related resource calls"""

    client_type: str = 'ecs'
    _list:dict = {
        'clusters': ApiCaller('list_clusters', 'clusterArns', 'clusterArn'),
        'services': ApiCaller('list_services', 'serviceArns', 'serviceArn'),
        'tasks': ApiCaller('list_tasks', 'taskArns', 'taskArn'),
    }
    _describe:dict = {
        'clusters': ApiCaller('describe_clusters', 'cluster', 'clusterArn'),
        'services': ApiCaller('describe_services', 'services', 'serviceArn'),
        'tasks': ApiCaller('describe_tasks', 'tasks', 'taskArn'),
    }



    async def get_all_untagged(self, region_name:str) -> list:
        """
        Find all things, ecs uses nesting, so this is harder.
        Does cluster -> service -> task
        """
        untagged = []
        
        session = aioboto3.Session(region_name=region_name)        
        async with session.client(self.client_type, region_name=region_name) as client:
            # get cluster arns
            cluster_arns = await self._list.get('clusters').call(client)
            self.arns.extend(cluster_arns)
            # get cluster info for each arn, including the tags
            cluster_details = await self._describe.get('clusters').call(client, **{"clusters":cluster_arns})
            
            # append any untagged clusters to the list
            untagged.extend(
                self._untagged(cluster_details, "clusterArn")
            )
            
            for cluster_arn in cluster_arns:

                for item in ['services', 'tasks']:
                    # get list of 'item'
                    lister = self._list.get(item)
                    arns = await lister.call(client, cluster=cluster_arn)
                    self.arns.extend(arns)
                    
                    # describe each of the items to get their tags
                    describer = self._describe.get(item)
                    args = {
                        "cluster": cluster_arn,
                        f"{describer.result_key}": arns,
                        "include": ['TAGS']
                    }
                    details = await describer.call(client, **args)
                    # merge the arns to the main list
                    self.arns.extend(
                        [d.get(describer.id_key) for d in details]
                    )
                    # find untagged
                    untagged.extend(
                        self._untagged(details, describer.id_key)
                    )
                    
        return untagged

    async def all(self, region_name:str) -> list:
        """Return all the arns of all resources in the ec2 scope that don't contain tags"""
        arns = await self.get_all_untagged(region_name)

        return arns

    