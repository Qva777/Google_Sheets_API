<hr>

<h1>📍How to install: </h1>

> This project aims to provide automation for sorting and formatting
> data in a Google Sheets spreadsheet using the Google Sheets API.
> It includes functionality to sort data based on a specific column
> and update the spreadsheet with the sorted data. Additionally, it
> supports formatting cells, such as aligning cell contents
> horizontally to the center.


<!-- Google OAuth -->
<details><summary><h2>⚙️SET UP Google Sheets API:</h2></summary><br/>

<h3>If this step has already been completed, you can skip it.</h3>

<h4>[An article from Google about setting up](https://developers.google.com/sheets/api/quickstart/python)</h4>

<h4>Or use this video tutorial:
[Link](https://www.youtube.com/watch?v=zCEJurLGFRk&ab_channel=TechWithTim)</h4>

<h4>Check if it's enabled:<br>
[Google Sheets](https://console.cloud.google.com/apis/library/drive.googleapis.com)<br>
[Google Driver](https://console.cloud.google.com/apis/library/sheets.googleapis.com)

<h4>[Create credentials.json](https://console.cloud.google.com/apis/api/sheets.googleapis.com/credentials) > service
account > KEYS > ADD KEY JSON </h4>
<h4>Put credentials.json into Google_Sheets_API folder</h4>

<h4>Share "Your Table" with your
[service account email](https://console.cloud.google.com/apis/api/sheets.googleapis.com/credentials)</h4>

</details>
<!-- Google OAuth -->


<!-- Python -->
<details><summary><h2>🐍SET UP Project:</h2></summary><br/>

<h3>Insert this command into cmd/terminal (in .env file set correct values):</h3>

```
cd backend/
echo "Creating .env file..."
cat <<EOL > .env
# Get form url https://docs.google.com/spreadsheets/d/__HERE_IS_SHEET_ID__/edit#gid=0
SHEET_ID="..."
EOL
cd ..
```

<h3>Create a virtual environment </h3>

```
python3 -m venv venv
```

<h3>Activate it:</h3>

```
source venv/bin/activate
```

<h3>Install libraries:</h3>

```
pip install -r requirements.txt
```

</details>
<!-- Python -->


