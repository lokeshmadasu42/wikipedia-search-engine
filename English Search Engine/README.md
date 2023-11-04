English wikipedia search engine :

It actually involves two important stages in building the end to end information retrieval system, also called as "wikipedia search engine" on english wikipedia
dump of size nearly 100GB. First stage is to create the index file in a very efficient manner, which will essentially help us in retrieving the documents list/articles
list for the given input query. Second stage is the search operation, which has very low latency(delay in retrieval) requirement. In simpler terms, each token in
the input query needs be search in the index file that was created earlier.

For phase-1:

I have completed the index creation part and basic search query implementation (which supports both plain query and field query). And also , for creating the
index file on 1.6GB dump took around 300 to 400 secs. In this phase I have created only one index file, no other intermediate files.

For phase-2:

In this phase , we are given a wikipedia dump of size nearly 100GB. I have used the same indexing code which I used in the first phase to create the index files
for this large dump as well. This time I have created multiple intermediate files to balance the compute load and for other search benefits.
The code has taken around 10 hours to create the index files. 

Intially, I have created 45 intermediate files and id_title files and from those files I created character wise files. Ex. all the tokens which starts with 'a' will be moved to
the token_a.txt, like this I have done it for all the alphabets and digits.

Index_size is  = "15.1 GB"

So the total files would be from 45 to 26(a-z) , 0-9(digits).

ID to title secondary index files = 101
ID to secondary index file map    = 1
Index files starts with digit     = 10
A-Z secondary index file map      = 26
----------------------------------------
Total files                       = 128

Finally, I have created secondary index files for each_alphabets. Total files are 2764.

Folder hierarchy,

1) char_wise_files folder contains all the secondary index files.(2674)
2) Index.py code file
3) Search.py code file
4) Stats.tx file which contains the stats.
5) Readme.txt




##############################

1 - Time taken to create inverted index : 10.35 hours
2 - Number of inverted index files : 2764
3 - Number of tokens in inverted index : 14603681
4 - Inverted index size : 15.1 GB

