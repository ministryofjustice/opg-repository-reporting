import argparse


def get_args() -> argparse.Namespace:
    """ Return configure args Namespace """
    # date handling
    parser = argparse.ArgumentParser(description=
                    'Generate a list of repositories and teams that owns them with some ' \
                    'other meta data.')

    org_group = parser.add_argument_group("Orginisation details")
    org_group.add_argument('--organisation-slug',
                            help='Slug of org to use for permissions',
                            default= 'ministryofjustice',
                            required=True)
    org_group.add_argument('--organisation-token',
                            help='GitHub token which has org level access',
                            required=True)

    team_group = parser.add_argument_group("Team options.")
    team_group.add_argument('--team-slug',
                            help='GitHub slug of the team to use (can be a list, split by comma)',
                            default='opg',
                            required=True)


    return parser.parse_args()
