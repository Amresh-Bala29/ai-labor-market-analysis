# Download data from Azuna API and save it to a CSV file

#Libraries
import os
import json
import time
from pathlib import Path
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

#Load enviornment variables
ROOT = Path(__file__).resolve().parents[1]

#Load in enviornment variables
load_dotenv(ROOT/ ".env")

#Retrieve API credentials 
APP_ID = os.environ["ADZUNA_APP_ID"]
APP_KEY = os.environ["ADZUNA_APP_KEY"]

#Generate a timestamp
timestamp = datetime.now(timezone.utc).strftime("%m-%d-%H-%M")

#Define output directory
output_dir = ROOT/ "data"/ "raw"/ "adzuna"/ timestamp

# Create directory
output_dir.mkdir(parents = True, exist_ok = True)

#Job categories to collect data for
roles = [
    "software engineer",
    "data analyst",
    "financial analyst",
    "marketing analyst",
    "business analyst",
    "healthcare analyst"
]

#Loop through each role and page
for role in roles:
    for page in range(1,3):
        print(f"Role: {role}, Page: {page}")

        #API Endpoint
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"

        #Request params
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": role,
            "results_per_page": 50,
            "sort_by": "date",
            "max_days_old": 90
        }

        #Send HTTP Request
        response = requests.get(
            url,
            params = params,
            headers = {"Accept": "application/json"},
            timeout = 30
        )

        #Check HTTP for errors
        response.raise_for_status()

        #Extract JSON data
        data = response.json()
        jobs = data.get("results", [])

        #Save data locally
        filename = f"{role.replace(' ', '_')}_p{page}.json"
        filepath = output_dir / filename

        with filepath.open("w", encoding = "utf-8") as f:
            json.dump({
                "search_term": role,
                "fetched_at": timestamp,
                "response": data
            }, f, indent = 2)

        #Pagination and rate limits
        print(f"{role} | Page{page}: {len(jobs)} jobs")

        if len(jobs) < 50:
            break
        time.sleep(3)
