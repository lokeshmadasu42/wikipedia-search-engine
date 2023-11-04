# English Wikipedia Search Engine

## Overview

This project presents an end-to-end information retrieval system developed using the English Wikipedia dump, a dataset of approximately 100GB in size encompassing nearly 22 million wiki pages. The system's core functionality supports two types of queries: Plain queries and Field queries. The primary goal is to provide the top 10 relevant Wikipedia article titles for a given query. The project unfolds in two key stages: Index Creation and Search Operation.

### Plain query examples:

- Lionel Messi
- Barcelona

### Support for field queries:

Fields include Title, Infobox, Body, Category, Links, and References of a Wikipedia page.

### Field query examples:

- t:World Cup i:2018 c:Football – search for "World Cup" in Title, "2018" in Infobox, and "Football" in Category

## Stage 1: Index Creation

The initial stage of the project focuses on efficiently creating the index file, which is pivotal for retrieving a list of article titles relevant to a given query. This stage involves the following steps:

1. **Parsing:** The XML dump is parsed using an xml.sax parser to extract field-wise information.
2. **Preprocessing:** Text is standardized by converting it to lowercase, replacing non-ASCII characters with spaces, tokenizing the text, removing stop words, and applying stemming to obtain word roots.
3. **Inverted Index Creation:** An inverted index is created, listing words and their corresponding posting lists. This data is stored in multiple index files.

Example of the index file format:

sachin:d1-t1c2b7|d5-t1
tendulkar:d1-t1b1|d6-c1b1


- **Index Size Constraint:** The index size is limited to a maximum of one-fourth of the original dump size (100GB), making the index size less than 25GB. The created index size is 15.1GB.
- To optimize computational load and search efficiency, multiple intermediate files were generated. Index creation for this large dump took approximately 10 hours.
- Initially, 46 inverted index files and 46 id_to_title files were created, containing word-posting lists and article IDs with their titles.
- The 46 id_to_title files were combined into a single id_to_title file, sorted by article ID.
- Character-wise files were generated from the 46 inverted index files, resulting in 26 files for the letters A to Z and 10 files for digits 0-9.
- Final character-wise files were created, each containing unique words and their posting lists. This process was also applied to digit-wise files.
- To manage computational load and search efficiency, each character-wise file was split into 101 smaller files. For example, `token_a.txt` was split into `token_a_1.txt`, `token_a_2.txt`, and so on. This resulted in a total of 2626 character-wise files, 10 digit-wise files, and a single id_to_title file.
- Character-wise info files were generated for the 26 character-wise files, containing the first words of the corresponding 101 character-wise files.
- The single id_to_title file was split into 101 id_to_title files. Additionally, an `id_title_info.txt` file was created, listing the last words of all 101 id_to_title files.
- In total, there are 2764 index files, including 2626 character-wise files, 26 character-wise info files, 10 digit-wise files, and one `id_to_title_info` file.
