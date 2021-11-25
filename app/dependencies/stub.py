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
title: Dependencies / Software Packages
last_reviewed_on: $date
review_in: 3 months
---

# <%= current_page.data.title %>

This is the amalgated view of Github's repository insights 'dependencies' data centralised via the preview version of their API.

<div>
$table
</div>

### Notes

This was generated via [this script](https://github.com/ministryofjustice/opg-repository-reporting/blob/main/dependencies.py).

"""
    )
    content = template.substitute(date=now, table=report)
    f = open(f"{report_dir}/report.html.md.erb", 'w')
    f.write(content)
    f.close()
