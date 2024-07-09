#############################################################################################################
## Author: Alberto Becerra (abecerr1@bsc.es)
## Team: Life Sciences - Natural Language Processing for Biomedical Information Analysis (bsc14)

## Description:
# Script to retrieve Wikipedia articles of Biomedical entities extracted from DBpedia Knowledge Graph
# The script retrieves the Wikipedia articles of the entities for different languages

## Usage:
# Usage (retrieve 100 articles in english):
# >> python main.py --language en --limit 100 --output output
# Usage (retrieve 100 articles in all languages):
# >> python main.py --language all --limit 100 --output output
# Usage (retrieve all articles in all languages):
# >> python main.py --language all --output output
#############################################################################################################

import os
from datetime import datetime
import argparse

from src import config
from src.utils.retrieve import extract_save
parser = argparse.ArgumentParser()
parser.add_argument("--kb", type=str, default="wikidata", choices=["wikidata", "dbpedia"], help="Knowledge Base to retrieve the articles from (dbpedia or wikidata)")
parser.add_argument("--language", type=str, default="all", help="Language of the Wikipedia page")
parser.add_argument("--limit", type=int, default=None, help="Number of results per page")
parser.add_argument("--output", type=str, default="output", help="Output file")

args = parser.parse_args()

kb = args.kb
language = [args.language] if args.language != "all" else config.LS_CONSORTIUM
limit = args.limit
out_folder = args.output

# Create the output folder with the current date and time
out_folder = os.path.join(out_folder, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}")
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# Retrieve the Wikipedia articles and save them in the output folder
endpoint = config.WIKIDATA_ENDPOINT if kb == "wikidata" else config.DBPEDIA_ENDPOINT
query = config.WIKIDATA_QUERY if kb == "wikidata" else config.DBPEDIA_QUERY
print(f"Retrieving articles from {kb}...")
extract_save(endpoint, query, language, limit, out_folder, parallel=True)