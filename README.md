Welcome to Caravela
====================

In the 15th century the Portuguese built ships that could take her crews further a 
way from land than any previous vesel, empowering a generation of bold explorers and traders.In that spirit we've created Caravela to gain deeper insights about the web and how it's built. 

Think of us as a search engine that gives you answers to questions such as:

* What's the average size of a web page?
* Which javascript plugins are tho most popular?
* What font is trendy right now?
* How many pages contain invalid content?

We don't intend to answer just those questions. Our goal is to empower you to ask ones we have
not thought of and share your discoveries with the world. This guide will help you do just that. 
Using the code and instructions you find here, you can help us extract new insights  out of our 
web crawl data and visualize the results for others.

Overview
-------------

In a nutshell, Caravela runs a series of functions written in python over a massive set of  documents crawled from the web. These functions take this unstructured content and return zero or more label and discrete value pairs  extracted from the page.   For instance the function that extracts the size of a page in kilobytes from a page simply looks like this:

```python
def size(doc):
   "Returns the size of a document in kilobytes"
    yield 'size', len(doc['payload']) / 1024
```

The function simply takes a document and `yields` the label `size` and some number such as `1` if the document is 1k in size.

 




[crawl] -> [extract] -> [query] -> [visualize]

Extracting Features
-------------

Querying for data
----------------------

Visualizing the Results
---------------------------
