from datetime import datetime
from string import Template
import html

def erb(report_dir:str, report_file_path:str) -> None:
    """ Generate a file from report_file_path contents suitable for erb """
    now = datetime.utcnow().strftime("%Y-%m-%d")

    file_reader = open(report_file_path, 'r', encoding='utf-8')
    report = file_reader.read()
    file_reader.close()


    template = Template(
        """---
title: Software Packages
last_reviewed_on: $date
review_in: 3 months
---

# <%= current_page.data.title %>

This is the amalgated view of Github's repository insights 'dependencies' data centralised via the preview version of their API.

<div>
$table
</div>

### Notes

This was generated via [this script](https://github.com/ministryofjustice/opg-repository-reporting/blob/main/software_packages.py).

"""
    )
    content = template.substitute(date=now, table=report)
    content = html.unescape(content)
    file_writer = open(f"{report_dir}/report.html.md.erb", 'w', encoding='utf-8')
    file_writer.write(content)
    file_writer.close()
