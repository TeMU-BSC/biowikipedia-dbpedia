from SPARQLWrapper import SPARQLWrapper, JSON
import aiohttp
import asyncio
import aiofiles
from tqdm.asyncio import tqdm_asyncio
import os
import wikipediaapi
from tqdm import tqdm
from tenacity import retry, wait_exponential, stop_after_attempt, wait_fixed
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
# @retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def fetch_results(query: str, endpoint: str):
    '''Fetch results from DBpedia given a SPARQL query with retries'''
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

def get_wikipedia_text(title: str, lang: str = "en"):
    '''Fetch the text of a Wikipedia article given its title using wikipediaapi'''
    wiki_wiki = wikipediaapi.Wikipedia('Alberto (aaa@gmail.com)', lang, verify=False)
    page = wiki_wiki.page(title)
    
    if page.exists():
        return page.text
    else:
        return ""  # Return empty string if the page does not exist

async def fetch_text_parallel(results, lang, out_file):
    '''Fetch Wikipedia text in parallel using asyncio and aiohttp'''
    async with aiohttp.ClientSession() as session:
        tasks = []
        for result in results:
            tasks.append(fetch_text(session, result, lang, out_file))
        
        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            await task

# @retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
async def fetch_text(session, result, lang, out_file):
    '''Fetch text for a single result and write to the output file with retries'''
    try:
        text = await asyncio.to_thread(get_wikipedia_text, result['title']['value'], lang)
        title = result['title']['value']
        url = f"https://{lang}.wikipedia.org/wiki/{title.replace(' ', '_')}"
        async with aiofiles.open(out_file, "a") as f:
            await f.write(f"{title}\t{url}\t{repr(text)}\n")
    except Exception as e:
        print(f"Error fetching text for {result['title']['value']}: {e}")

def get_wikipedia_text_batch(results, lang, out_file=None, parallel=True):
    '''Fetch Wikipedia texts and write to a file'''
    if parallel:
        asyncio.run(fetch_text_parallel(results, lang, out_file))
    else:
        fetch_text_sequential(results, lang, out_file)

def fetch_text_sequential(results, lang, out_file):
    '''Fetch Wikipedia text sequentially'''
    for result in tqdm(results):
        try:
            # time.sleep(1.5)
            text = get_wikipedia_text(result['title']['value'], lang)
            title = result['title']['value']
            url = f"https://{lang}.wikipedia.org/wiki/{title.replace(' ', '_')}"
            with open(out_file, "a") as f:
                f.write(f"{title}\t{url}\t{repr(text)}\n")
        except Exception as e:
            print(f"Error fetching text for {result['title']['value']}: {e}")

def extract_save(endpoint, query, ls_langs, limit, out_folder, parallel=True):
    '''Extract and save Wikipedia texts from DBpedia results'''
    if limit is None:
        limit = int(1E8)
        print("Retrieving all articles...")

    max_batch = 10_000
    if limit < max_batch:
        pages = 1
    else:
        pages = (limit // max_batch + 1)
        limit = max_batch

    for lang in ls_langs:
        processed = 0
        for page in range(pages):
            print(f"Retrieving articles in {lang} -- Page: {page} -- Processed: {processed}...")
            rep_query = adapt_query(query, lang, N=limit, offset=(page * limit))
            results = fetch_results(rep_query, endpoint=endpoint)
            out_file = os.path.join(out_folder, f"corpus_{lang}.txt")
            get_wikipedia_text_batch(results, lang, out_file=out_file, parallel=parallel)
            n_results = len(results)
            processed += n_results
            if n_results < limit:
                break

def adapt_query(query, lang, N=10, offset=0):
    '''Adapt the SPARQL query with the language, limit, and offset'''
    lang_query = query.replace('<LANGUAGE>', lang)
    limit_lang_query = lang_query.replace('<N>', str(N))
    offset_limit_lang_query = limit_lang_query.replace('<OFFSET>', str(offset))
    return offset_limit_lang_query
