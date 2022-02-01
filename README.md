# opg-repository-reporting

Repository of python tooling to report on our organisations repositories for certain types of data that we then use for reporting to project and delivery teams.

Note: This assumes the active cli has correct permissions on github to run these commands.

## Release Report

Generates a data set containg the number of merges made into each repositories default branch (`main` normally), grouped by the month for a set time period.

Found at `./releases.py`

### Usage

Typically, you will want to run a command like this:

```python ./releases.py --organisation-token ${GITHUB_TOKEN} --organisation-slug ministryofjustice --team-slug opg ```

This will create report for the last 6 months for the `ministry of justice` github organisation, limited to the `opg` teams repositories and output the information as markdown.


## Ownership Report

Generate a report of what teams own which repositories based on root organization and team.

Found at `./owners.py`

### Usage

Typically, you will want to run a command like this:

```python ./owners.py --organisation-token ${GITHUB_TOKEN} ```

This will create a markdown file containing a list of repositories, their associated teams and some meta data (like last commit date).


## Meta Report

Generate a report of all accessible repositories containing commit dates, default branches and similar data.

Found at `./meta.py`

### Usage

Typically, you will want to run a command like this:

```python ./meta.py --organisation-token ${GITHUB_TOKEN} ```

This will create a markdown file.



## Software Packages Report

Uses Github preview api to generate a list of all detected software dependencies within all the repositories the token is authorised to access with the team.


```python ./software_packages.py --organisation-token ${GITHUB_TOKEN} ```
