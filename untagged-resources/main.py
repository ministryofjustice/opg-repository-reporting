from process_args import process_args
from custom_aws import service_list, ServiceClasses
from pprint import pprint
import asyncio



async def main():
    """Async execution"""

    args = process_args()
    services = await service_list(args.region)
    found = {}
    for service in services:
        service_instance = ServiceClasses.get(service)
        if service_instance is not None:
            found.setdefault(service, await service_instance.all(args.region) )

        #get_service_class(service, args.region)
    



#
asyncio.run(main())

# client = boto3.client('resourcegroupstaggingapi', region_name=args.region)

# untagged:list = []
# for resource in client.get_resources().get('ResourceTagMappingList'):
#     tags:list = resource.get('Tags')
#     arn:str = resource.get('ResourceARN')
#     if len(tags) == 0:
#         untagged.append(arn)

# pprint(untagged)
