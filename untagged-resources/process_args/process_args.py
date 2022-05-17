import argparse
from argparse import Namespace

def process_args() -> Namespace:
    """Handle input arguments for this code"""

    description:str = """
    Find untagged resources from the resource groups within the account and region.
    For local use only - presumes aws-vault usage for authentication
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--region',
                            help='AWS region to run within. (default: eu-west-1)',
                            default='eu-west-1')
                           
    return parser.parse_args()
