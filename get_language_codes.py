from SPARQLWrapper import SPARQLWrapper
from src.utils.retrieve import fetch_results

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX sdo: <https://schema.org/>

    SELECT ?lang ?iso6391Code
    WHERE {
      ?lang a dbo:Language ;
      dbo:iso6391Code ?iso6391Code .
      FILTER (STRLEN(?iso6391Code)=2) # to filter out non-valid values
    }
"""
results = fetch_results(query)
for result in results:
    print("\t".join([result[item]['value'] for item in result]), end="\n", file=open("languages.tsv", "a"))