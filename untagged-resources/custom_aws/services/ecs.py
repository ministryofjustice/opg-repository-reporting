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



    async def get_all(self, region_name:str) -> dict:
        """
        Find all things, ecs uses nesting, so this is harder.
        Does cluster -> service -> task
        """
        untagged = []
        all_resources = []

        session = aioboto3.Session(region_name=region_name)
        async with session.client(self.client_type, region_name=region_name) as client:
            # get cluster arns
            cluster_arns = await self._list.get('clusters').call(client)
            all_resources.extend(cluster_arns)
            # get cluster info for each arn, including the tags
            cluster_details = await self._describe.get('clusters').call(client, **{"clusters":cluster_arns})
            
            # append any untagged clusters to the list
            untagged_clusters = self._untagged(cluster_details, "clusterArn")
            untagged.extend( untagged_clusters )
            
            print(f"\t - [list_clusters]\n\t\t All: [{(len(cluster_arns))}]\t Untagged: [{len(untagged_clusters)}]")
            
            for cluster_arn in cluster_arns:

                for item in ['services', 'tasks']:
                    # get list of 'item'
                    lister = self._list.get(item)
                    arns = await lister.call(client, cluster=cluster_arn)
                    all_resources.extend(arns)                    
                    
                    # describe each of the items to get their tags
                    describer = self._describe.get(item)
                    args = {
                        "cluster": cluster_arn,
                        f"{describer.result_key}": arns,
                        "include": ['TAGS']
                    }
                    details = await describer.call(client, **args)
                    # merge the arns to the main list
                    all_resources.extend(
                        [d.get(describer.id_key) for d in details]
                    )
                    # find untagged
                    no_tags = self._untagged(details, describer.id_key)
                    untagged.extend(no_tags)
                    print(f"\t - [list_{item}]\n\t\t All: [{(len(arns))}]\t Untagged: [{len(no_tags)}]")
                    
        return {'untagged': untagged, 'all': all_resources}

    async def all(self, region_name:str) -> dict:
        """Return all the arns of all resources in the ec2 scope that don't contain tags"""
        return await self.get_all(region_name)


    