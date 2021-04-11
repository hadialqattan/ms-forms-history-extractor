from urllib.parse import urlparse, parse_qs
from datetime import datetime as dt
import traceback
import json
import os

MILLION = 10 ** 6
SEMESTER_BEGINNING_TIMESTAMP_MICROSECONDS = (
    dt.strptime("2021-01-17", "%Y-%m-%d").timestamp() * MILLION
)

while True:
    try:
        FILE_PATH = input("Enter `BrowserHistory.json` file path: ")
    except KeyboardInterrupt:
        print("\n\nBye bye!")
    try:
        with open(FILE_PATH, "r") as f:
            data = json.loads(f.read())
        break
    except FileNotFoundError as err:
        print(f"Wrong file path: {err}")

try:
    ms_forms, ids, internal_id = [], set(), 1
    for d in data["Browser History"]:
        if d["time_usec"] > SEMESTER_BEGINNING_TIMESTAMP_MICROSECONDS:
            if "https://forms.office.com/pages/responsepage" in d["url"].lower():
                url_id = parse_qs(urlparse(d["url"]).query)["id"][0]
                if url_id not in ids:
                    date = dt.fromtimestamp(d["time_usec"] / MILLION).strftime(
                        "%Y-%m-%d"
                    )
                    ms_forms.append(
                        {
                            "id": internal_id,
                            "form_id": url_id,
                            "url": d["url"],
                            "date": str(date),
                        }
                    )
                    ids.add(url_id)
                    internal_id += 1
except KeyError as err:
    print(
        f"Invalid `BrowserHistory.json` file, "
        "make sure you got this file from https://takeout.google.com/ correctly!"
    )
    print(traceback.print_exc())


html: str = """<!DOCTYPE html>
<html lang="en">
<head>
	<title>Your Forms</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->
	<link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="css/util.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
<!--===============================================================================================-->
</head>
<body>

	<div class="limiter">
		<div class="container-table100">
			<div class="wrap-table100">
				<div class="table100">
					<table>
						<thead>
							<tr class="table100-head">
                <th class="column1">ID</th>
								<th class="column2">URL</th>
								<th class="column3">Date</th>
							</tr>
						</thead>
						<tbody id="table-body">
								{table_rows}
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>

<!--===============================================================================================-->
	<script src="vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/bootstrap/js/popper.js"></script>
	<script src="vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/select2/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="js/main.js"></script>

</body>
</html>
"""
html_tr: str = """<tr>
    <td class="column1">{id}</td>
    <td class="column2">
    <a href="{url}" target="_blank" rel="noopener noreferrer">{form_id}</a>
    </td>
    <td class="column3">{date}</td>
</tr>
"""
INDEX_PATH = os.path.abspath("./webview/index.html")
with open(INDEX_PATH, "w+") as index_html:
    table_rows: str = "\n"
    for d in ms_forms:
        table_rows += html_tr.format(
            id=d["id"], url=d["url"], form_id=d["form_id"], date=d["date"]
        )
    index_html.write(html.format(table_rows=table_rows))

print(f"\nPlease open this file using any browser:\n{INDEX_PATH}")

input("\npress any key to exit...")
