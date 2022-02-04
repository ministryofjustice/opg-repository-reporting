from datetime import datetime
from string import Template
import html

def erb(report_dir:str, report_file_path:str) -> None:
    """ Generates string from template with report_file_path content used """
    now = datetime.utcnow().strftime("%Y-%m-%d")

    file_reader = open(report_file_path, 'r', encoding='utf-8')
    report = file_reader.read()
    file_reader.close()

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
    file_writer = open(f"{report_dir}/report.html.md.erb", 'w', encoding='utf-8')
    file_writer.write(content)
    file_writer.close()
