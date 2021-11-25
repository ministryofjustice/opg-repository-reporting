from datetime import datetime
from string import Template
import html

def erb(report_dir:str, report_file_path:str) -> str:
    """
    """
    now = datetime.utcnow().strftime("%Y-%m-%d")

    f = open(report_file_path, 'r')
    report = f.read()
    f.close()

    template = Template(
        """---
title: Owners
last_reviewed_on: $date
review_in: 3 months
---

# <%= current_page.data.title %>

Listing of all our repositorys, team that owns them and their current status.

<div>
$table
</div>

### Notes

This was generated via [this script](https://github.com/ministryofjustice/opg-repository-reporting/blob/main/owners.py).

"""
    )
    content = template.substitute(date=now, table=report)
    content = html.unescape(content)
    f = open(f"{report_dir}/report.html.md.erb", 'w')
    f.write(content)
    f.close()
