# Notes

```
LS_CONSORTIUM = ['en', # English
                 'es', # Spanish
                 'cs', # Cestina
                 'it', # Italian
                 'ro', # Romanian
                 'sv', # Swedish
                 'nl'  # Dutch
                 ]
```

DBPEDIA QUERY

```
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT (COUNT(?subject) AS ?count)
WHERE {
  { ?subject a dbo:Disease . }
  UNION
  { ?subject a dbo:Drug . }
  UNION
  { ?subject a dbo:MedicalCondition . }
  UNION
  { ?subject a dbo:AnatomicalStructure . }
  ?subject foaf:isPrimaryTopicOf ?wikiPageURL .
  ?subject rdfs:label ?title .
  FILTER (lang(?title) = "sv")
}
```

- English: 37604 results (in batches of 10_000)
- Spanish: 509549 results (in batches of 10_000)
- Czech: 264789 results (in batches of 10_000)
- Italian: 493822 results (in batches of 10_000)
- Romanian: 0 results
- Swedish: 254091 results
- Dutch: 343819 results (in batches of 10_000)

WIKIDATA QUERY

https://datos.gob.es/es/blog/wikidata-una-base-de-datos-de-conocimiento-libre-y-abierto

- English: 1831 results
- Spanish: 678 results
- Czech: 215 results
- Italian: 609 results
- Romanian: 133 results
- Swedish: 299 results
- Dutch: 640 results

