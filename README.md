Welcome to Caravela
====================

In the 15th century the Portuguese built ships  that could take her crews further from land than any previous vesel, empowering a generation of bold explorers and traders.In that spirit we've created Caravela to gain deeper insights about the web and how it's built. 

Think of us as a search engine that gives you answers to questions such as:

* What's the average size of a web page?
* Which javascript plugins are tho most popular?
* What font is trendy right now?
* How many pages contain invalid content?

We don't intend to answer just those questions. Our goal is to empower you to ask ones we have not thought of and share your discoveries with the world. This guide will help you do just that.  Using the code and instructions you find here, you can help us extract new insights  out of our web crawl data and visualize the results for others.


Overview
-------------


[crawl] -> [extract] -> [query] -> [visualize]


Extracting Features
-------------

In a nutshell, Caravela runs a series of functions written in python over a massive set of  documents crawled from the web. These functions take this unstructured content and return zero or more label and discrete value pairs, which we call *features*,  from the page.   For instance the function that extracts the size of a page in kilobytes from a page simply looks like this:

```python
def size(doc):
    "Returns the size of a document in kilobytes"
    yield 'size', len(doc['payload']) / 1024
```

The function simply takes a document and `yields` the label `size` and some number such as `1` if the document is 1k in size. You can see it in action in the python interpretor.

```python
>>> doc = {'payload': 'The quick brown fox'}
>>> list(size(doc))
[('size', 0)]
```

Note that we use python's `yield` statement to iteratively return the features from the document bit by bit in a memory efficient manner.  Hence the need to  convert the results  to a list before displaying them. You can `yield` more than one feature from your function. For example here's a function that extracts each header in the document along with the headers value:

```python
def size(doc):
    "Returns the headers from the given document."
    for header,value in doc['headers'].items():
        yield 'header', "%s:%s" % (header, value)
```

You might even be tempted to yield every word found in the document! But uh.. there's plenty of others already doing that sort of thing now isn't there?

Here's an overview of the whole process. A series of documents are run through a  series of functions that builds up a list of extracted features from those documents. As depicted in Figure 1

![Figure 1: Extraction Overview](/docs/imgs/extraction_overview.png "Figure 1: Extraction Overview")


These *features* are collected into a data structure known as an inverted index which we can 
query later on and use the results to build interesting visuals.






Querying for data
----------------------

Visualizing the Results
---------------------------
