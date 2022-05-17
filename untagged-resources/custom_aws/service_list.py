import aioboto3

async def service_list(region_name:str) -> list:
    """Uses the region passed to return all available services."""
    session = aioboto3.Session(region_name=region_name)
    return session.get_available_services()
