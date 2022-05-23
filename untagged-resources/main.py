import asyncio
from pprintpp import pprint

from process_args import process_args
from custom_aws import service_list, ServiceClasses


async def main():
    """Async execution"""

    args = process_args()
    services = await service_list(args.region)
    found = {}
    total_resources:int = 0
    untagged_resources:int = 0
    for service in services:        
        service_instance = ServiceClasses.get(service)
        if service_instance is not None:
            print(f"[{service}]")
            service_result = await service_instance.all(args.region)
            found.setdefault(service, service_result)
            found_count:int = len(service_result.get('all', []) )
            untagged_count:int = len(service_result.get('untagged', []) )

            print(f"\n\tAll: [{found_count}] Untagged: [{untagged_count}]\n")

            total_resources = total_resources + found_count
            untagged_resources = untagged_resources + untagged_count

    print(f"\nTOTALS:\n All: [{total_resources}] Untagged: [{untagged_resources}]\n")

asyncio.run(main())

# client = boto3.client('resourcegroupstaggingapi', region_name=args.region)

# untagged:list = []
# for resource in client.get_resources().get('ResourceTagMappingList'):
#     tags:list = resource.get('Tags')
#     arn:str = resource.get('ResourceARN')
#     if len(tags) == 0:
#         untagged.append(arn)

# pprint(untagged)
