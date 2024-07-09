LS_CONSORTIUM = ['en', # English
                 'es', # Spanish
                 'cs', # Cestina
                 'it', # Italian
                 'ro', # Romanian
                 'sv', # Swedish
                 'nl'  # Dutch
                 ]

DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql"
WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

DBPEDIA_QUERY = """
                PREFIX dbo: <http://dbpedia.org/ontology/>

                SELECT ?subject ?title lang(?title) ?wikiPageURL
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
                FILTER (lang(?title) = "<LANGUAGE>")
                }
                LIMIT <N>
                OFFSET <OFFSET>
                """

WIKIDATA_QUERY = """
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                PREFIX wikibase: <http://wikiba.se/ontology#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX schema: <http://schema.org/>

                SELECT ?subject ?title ?wikiPageURL
                WHERE {
                { ?subject wdt:P31 wd:Q12136 . }        # Disease
                UNION
                { ?subject wdt:P31 wd:Q11173 . }        # Drug
                UNION
                { ?subject wdt:P31 wd:Q713623 . }       # Medical condition
                UNION
                { ?subject wdt:P31 wd:Q4936952 . }      # Anatomical structure
                ?subject rdfs:label ?title .
                FILTER (lang(?title) = "<LANGUAGE>")
                ?article schema:about ?subject .
                ?article schema:isPartOf <https://<LANGUAGE>.wikipedia.org/> .
                BIND(STR(?article) AS ?wikiPageURL)
                }
                LIMIT <N>
                OFFSET <OFFSET>
                """