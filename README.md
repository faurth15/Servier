# Servier


## Part 1 - Python

### Servier class

>- This class is used to extract the articles for each drug. This class contains 3 functions:
>>- create_graph(): This function create a Dataframe in order to represent the graph. We choose to represent the graph as a Dataframe because we can easily convert it to json
and it is easier to handle.
>>- preprocessing(): preprocess the dataset in order to avoid duplicates and remove useless rows in order to gain some times if we deal with larger datset.
>>- Extraction(): For each drug extract the articles that quotes it.

>- Extraction and preprocessing functions deal with one dataset at a time. I choose to built them like that in order to parallelize the execution for each dataset.
Indeed, the graph is created of such a way that we can be filled simultaneously with the medical publications and the scientific articles. We then apply 'set' to the newspaper column
in order to avoid counting it twice (in the case two articles in the same newspaper quote the same drug the same day).

### Adhoc

>- very simple function that gets all the newspapers in our graph and use Counter to have the number of occurences for each newspaper.


### To go further

>- We already say that the code can be parallelize. We can easily change that by using the multiprocessing library of python.
>- Moreover my code is computing the whole dataset at each time. We can try to modified it in such a way that we can call it just for pieces of the dataset (for example add a features to compute only some rows)

## Part 2 - SQL

>- See SQL.sql file
