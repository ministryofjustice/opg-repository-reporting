from datetime import datetime
from string import Template
import html

def erb(report_dir:str, report_file_path:str) -> None:
    """
    Return a formatted string based on the erb template style using content from report_file_path 
    """
    now = datetime.utcnow().strftime("%Y-%m-%d")

    file_reader = open(report_file_path, 'r', encoding='utf-8')
    report = file_reader.read()
    file_reader.close()


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
    content = html.unescape(content)
    file_writer = open(f"{report_dir}/report.html.md.erb", 'w', encoding='utf-8')
    file_writer.write(content)
    file_writer.close()
