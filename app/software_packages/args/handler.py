import argparse


def get_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description='Generate a report of all package dependencies.')

    org_group = parser.add_argument_group("Orginisation details")
    org_group.add_argument('--organisation-slug',
                        help='Slug of org to use for permissions',
                        default= 'ministryofjustice',
                        required=True)
    org_group.add_argument('--organisation-token',
                        help='GitHub token which has org level access',
                        default='opg',
                        required=True)

    team_group = parser.add_argument_group("Team options.")
    team_group.add_argument('--team-slug',
                        help='GitHub slug of the team to run against (can be a list, split by comma)',
                        required=True)

    data_group = parser.add_argument_group("Data options.")
    data_group.add_argument('--filter',
                        help='Filter repositories by this list of names',
                        default='*')


    return parser.parse_args()
