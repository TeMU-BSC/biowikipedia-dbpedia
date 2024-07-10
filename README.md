# Wikipedia Article Retrieval Project

## Main Goal
The primary objective of this project is to retrieve filtered information from Wikipedia using semantic querying techniques. It focuses on extracting Wikipedia articles of biomedical entities from knowledge graphs, specifically targeting entities extracted from DBpedia and Wikidata. This allows for the efficient gathering of relevant information across different languages, tailored to the user's requirements.

## What are Knowledge Graphs?
Knowledge graphs represent a collection of interlinked descriptions of entities – objects, events, or concepts. These graphs not only store factual information but also the relationships between these entities. They are a powerful tool for semantic querying, enabling complex questions to be answered with high precision and facilitating a deeper understanding of the data.

## DBpedia and Wikidata
- **DBpedia**: A crowd-sourced community effort to extract structured content from the information created in Wikipedia. It allows users to semantically query relationships and properties of Wikipedia resources, including links to other related datasets.
- **Wikidata**: A free and open knowledge base that can be read and edited by both humans and machines. Wikidata acts as central storage for the structured data of its Wikimedia sister projects including Wikipedia, Wikivoyage, Wiktionary, Wikisource, and others.

## Output
The output of this project is a collection of Wikipedia articles related to biomedical entities. These articles are retrieved based on the specified parameters such as the knowledge base (DBpedia or Wikidata), language, and the number of results. The output is saved in a designated folder, organized with a timestamp to ensure uniqueness and ease of access.

## How to Run
To run this script, you need Python 3.10 installed on your system (if you use another version, the requirements versions may not be compatible). You can execute the script from the command line by navigating to the project directory and running one of the following commands based on your requirements:

- To retrieve 100 articles in English:
```bash
python main.py --language en --limit 100 --output output
```
- To retrieve 100 articles in all languages:
```bash
python main.py --language all --limit 100 --output output
```
- To retrieve all articles in all languages:
```bash
python main.py --language all --output output
```

Ensure you have all the necessary dependencies installed by running `pip install -r requirements.txt` before executing the script.

This project simplifies the process of accessing and utilizing the vast amount of information available on Wikipedia and other knowledge bases.

## Set Project Variables
The `config.py` file contains configuration variables for a Python project aimed at querying Wikipedia information related to biomedical entities from DBpedia and Wikidata. Here's an explanation of each variable and how to set them:

- **LS_CONSORTIUM**: This is a list of language codes representing the languages in which you want to retrieve information. Each language is represented by its ISO 639-1 code (e.g., 'en' for English, 'es' for Spanish). You can modify this list by adding or removing language codes according to your requirements.

- **DBPEDIA_ENDPOINT**: This variable holds the URL of the DBpedia SPARQL endpoint. It is used to send SPARQL queries to DBpedia. The default value is set to "http://dbpedia.org/sparql". Generally, this value does not need to be changed unless DBpedia updates its query endpoint URL.

- **WIKIDATA_ENDPOINT**: Similar to DBPEDIA_ENDPOINT, this variable contains the URL for the Wikidata SPARQL endpoint ("https://query.wikidata.org/sparql"). It is where SPARQL queries are sent to retrieve information from Wikidata. This URL typically remains constant.

- **DBPEDIA_QUERY**: This is a multi-line string that defines the SPARQL query template for querying DBpedia. It is designed to select subjects and their titles in a specified language, filtering by entity types such as Disease, Drug, Medical Condition, and Anatomical Structure. The placeholders <LANGUAGE>, <N>, and <OFFSET> are meant to be replaced with the desired language code, the limit on the number of results, and the offset for pagination, respectively, at runtime.

- **WIKIDATA_QUERY**: This variable also contains a SPARQL query template, but it is for querying Wikidata. It selects subjects, their titles, and their Wikipedia URLs, filtering by the same types of biomedical entities as the DBpedia query. Unlike the DBpedia query, this template ends abruptly and seems to be missing the closing parts of the query, including filtering by language, limiting the number of results, and specifying the offset for pagination.

To set or modify these variables:

For simple variables like DBPEDIA_ENDPOINT and WIKIDATA_ENDPOINT, you can directly change the URL strings if necessary.
For the LS_CONSORTIUM list, add or remove the string elements containing the language codes as needed.
For the SPARQL query templates (DBPEDIA_QUERY and WIKIDATA_QUERY), you can modify the query structure or the entity types being queried. To use the placeholders effectively, ensure that your code replaces <LANGUAGE>, <N>, and <OFFSET> with dynamic values based on your application's requirements.