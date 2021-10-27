# opg-repository-reporting

Repository of python tooling to report on our organisations repositories for certain types of data that we then use for reporting to project and delivery teams.

Note: This assumes the active cli has correct permissions on github to run these commands.

## Merge Report

Generates a data set containg the number of merges made into each repositories default branch (`main` normally), grouped by the month for a set time period.

Found at `./merge_report.py`

### Usage


Typically, you will want to run a command like this:

```python ./merge_report.py --organization ministryofjustice --team opg --type csv```

This will create report for the last 6 months for the `ministry of justice` github organisation, limited to the `opg` teams repositories and output the information as a `csv` to a file.

#### Options

`--organization` sets the GitHub organisation to be looking at (default: `ministryofjustice`).

`--team` set the GitHub team (should be part of the above organisation) to find repositories for (default: `opg`).

`--type` set the report output format, can be `csv` or `md` (default: `md`).

`--filename` set the filename (without extension) that will be created (default: `merge_counts`).

`--start` sets the start date of the report (default: `-6 months`).

`--end` sets the end date of the report (default: `now()`).


## Ownership Report

Generate a report of what teams own which repositories based on root organization and team.

Found at `./ownership_report.py`

### Usage

Typically, you will want to run a command like this:

```python ./ownership_report.py  --type md```

This will create a markdown file containing a list of repositories, their associated teams and some meta data (like last commit date).

#### Options

`--organization` sets the GitHub organisation to be looking at (default: `ministryofjustice`).

`--team` set the GitHub team (should be part of the above organisation) to find repositories for (default: `opg`).

`--type` set the report output format, can be `csv` or `md` (default: `md`).

`--filename` set the filename (without extension) that will be created (default: `merge_counts`).



## Tooling Report

This is no longer used, please see the [replacement github action instead](https://github.com/ministryofjustice/opg-repository-scanner).




Development repository: Managed by opg-org-infra &amp; Terraform
