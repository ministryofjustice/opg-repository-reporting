from datetime import datetime
from string import Template


def erb(report_dir:str, report_file_path:str) -> str:
    """
    """
    now = datetime.utcnow().strftime("%Y-%m-%d")

    f = open(report_file_path, 'r')
    report = f.read()
    f.close()


    template = Template(
        """---
title: Releases
last_reviewed_on: $date
review_in: 3 months
---

# <%= current_page.data.title %>

As we run CD/CI pipelines on our repositories for ease we class a merge to the default branch as a release.

The table below shows the last six months.

<div>
$table
</div>

### Notes

This was generated via [this script](https://github.com/ministryofjustice/opg-repository-reporting/blob/main/releases.py).

"""
    )
    content = template.substitute(date=now, table=report)
    f = open(f"{report_dir}/report.html.md.erb", 'w')
    f.write(content)
    f.close()
