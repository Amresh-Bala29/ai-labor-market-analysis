# Download data from Azuna API and save it to a CSV file

#Libraries
import os
import json
import time
from pathlib import Path
import requests
from dotenv import load_dotenv