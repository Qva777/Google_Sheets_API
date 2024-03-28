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

<h4><a href="https://developers.google.com/sheets/api/quickstart/python">An article from Google about setting
up</a></h4>
<h4>Or use this <a href="https://www.youtube.com/watch?v=zCEJurLGFRk&ab_channel=TechWithTim">video tutorial</a>.</h4>

<h4>Check if it's enabled:</h4>

<a href="https://console.cloud.google.com/apis/library/drive.googleapis.com"><h4>Google Sheets</h4></a>
<a href="https://console.cloud.google.com/apis/library/sheets.googleapis.com"><h4>Google Drive</h4></a>
<h4><a href="https://console.cloud.google.com/apis/api/sheets.googleapis.com/credentials">Create credentials.json</a> >
service account > KEYS > ADD KEY JSON</h4>

<h4>Put credentials.json into Google_Sheets_API folder</h4>

<h4>Share "Your Table" with your <a href="https://console.cloud.google.com/apis/api/sheets.googleapis.com/credentials">
service account email</a></h4>

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


<h3>Run:</h3>

```
python main.py
```

</details>
<!-- Python -->


