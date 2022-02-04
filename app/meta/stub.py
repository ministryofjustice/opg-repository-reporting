from datetime import datetime
from string import Template
import html

def erb(report_dir:str, report_file_path:str) -> str:
    """ Creates a erb file using data from the report_file_path """
    now = datetime.utcnow().strftime("%Y-%m-%d")

    file_handler = open(report_file_path, 'r', encoding='utf-8')
    report = file_handler.read()
    file_handler.close()

    template = Template(
        """---
title: Meta
last_reviewed_on: $date
review_in: 3 months
---

# <%= current_page.data.title %>

Listing of all our repositories and meta data.

<div>
$table
</div>

### Notes

This was generated via [this script](https://github.com/ministryofjustice/opg-repository-reporting/blob/main/meta.py).

"""
    )
    content = template.substitute(date=now, table=report)
    content = html.unescape(content)
    f = open(f"{report_dir}/report.html.md.erb", 'w', encoding='utf-8')
    f.write(content)
    f.close()
