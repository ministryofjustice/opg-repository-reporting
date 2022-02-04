import argparse
import datetime
import dateutil.relativedelta



def get_args() -> argparse.Namespace:
    """ Return a configure args namespace """
    # date handling
    now = datetime.datetime.utcnow()
    start = now - dateutil.relativedelta.relativedelta(months=6)
    start = start.replace(day=1, hour=0, minute=0, second=0)

    parser = argparse.ArgumentParser(description=
                'Generate a report of merges to the default branch '\
                '- grouped by month - by repo.')

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

    data = parser.add_argument_group("Data options.")

    data.add_argument('--filter',
                        help='Filter repositories by this list of names',
                        default='*')

    # start & end date of the report
    data.add_argument("--start",
                            type=datetime.date.fromisoformat,
                            default=start,
                            help=f"Set the start date for this report (default: {start.strftime('%Y-%m-%d')})")
    data.add_argument("--end",
                            type=datetime.date.fromisoformat,
                            default=now,
                            help=f"Set the end date for this report (default: {now.strftime('%Y-%m-%d')})")


    return parser.parse_args()
