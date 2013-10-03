Published Insights
-----------------

The first thing you'll see when you login is a list of "Insights" published by other Caravela users.

![Published Insights][0]

 
Insights are visuals of data queries along with a short description of the information the author is trying to show. A great way to learn how to create an Insight is exploring what others have done, so go ahead and click on one!

Viewing an Insight
------------------

![Design an Insight][1]


An Insight visualizes (graphs) the resulst of a query and gives the author a chance to describe the information it's showing. We'll cover how to create a graph shortly,  first we need to learn how to query  and manipulate data. To do that click on the "Data" button to see  the query and underlying data that was used to create the Insight you are looking at.


Querying data
-------------

You can query Caravela data using a form of SQL, inspired by Google's Big Query, thanks to the [Splicer Library][4].

![Querying Data][2]


The interface let's you issue queries and page through the results. For example to see a subset of the data that's available write the following query.

```
select * from docs
```

This returns the first 100 documents in our dataset.

We provide a number of tables and views, which you can query  and mash together.  For instance, we've created a view that returns a list of all the urls that were include as scripts along with number of pages they were included on. To query that view simply write.

```
select * from scripts
```

As we mentioned, scripts is just a view, it's equivalent to the following query

```
select scripts as script, count()
from flatten(docs, 'scripts')
group by script
order by count desc
```

An upcoming feature will enable users to save views directly within the browser.  If you have a view that you think others will find useful, fork the Caravela Project on GitHub, add the view to db.py and submit a pull request. We'll be sure to include it!

For more information on querying see the [Splicer Docs][5]

Exploring Data
--------------

To see what type of data is available to query click on "Data" under the "Browse" section on the left hand side of the page. From here you'll see the various tables of data we are providing along with their schemas.


![Exploring Data][3]


Currently we're providing a corpus of web documents gathered by Common Crawl. There's allot more data we will be providing in the future. We plan on making data available based on the included CSS and Javascript as it's interpreted by the browser at runtime. So keep an eye on this section.

Visualizing Data
----------------

With the data in hand it's time to  visualize it. Click on the "Visualize" button from the Query page.
This returns you to the insight view. We're using visualization grammar by Trifacta known as [Vega][6]. 
Here's an example json document. You'll notice that we've made one extention. We've added the the query 
attribute. The results of which are bounded as the `document` data set.


```javascript
{
  "query": "select * from scripts where find(script, 'jquery') >= 0 limit 10",
   "description": "A listing of all scripts with the word jquery in it. I need to create a method to extract the plugin name from the urls.",
  "name": "JQuery Plugin",
  "width": 480,
  "height": 200,
  "padding": {"top": 10, "left": 300, "bottom": 20, "right": 10},
  "data": [
    {
      "name": "documents",
      "-transform":[{"type": "filter", "test": "d.data.script"}]
    }
    ],
  "scales": [
    {"name":"y", "type":"ordinal", "range":"height", "domain":{"data":"documents", "field":"data.script"}},
    {"name":"x",  "range":"width", "nice":true, "domain":{"data":"documents", "field":"data.count"}}
  ],
  "axes": [
    {"type":"x", "scale":"x"},
    {"type":"y", "scale":"y"}
  ],
  "marks": [
    {
      "type": "rect",
      "from": {"data":"documents"},
      "properties": {
        "enter": {
          "x": {"scale":"x", "field":"data.count"},
          "x2": {"scale":"y", "value":0},

          
          "y": {"scale":"y", "field":"data.script"},
          "height": {"scale":"y", "band":true, "offset":-1}
          
        },
        "update": { "fill": {"value":"steelblue"} },
        "hover": { "fill": {"value":"red"} }
      }
    }
  ]
}
```

Vega gives us allot of flexability to creat custom charts, and graphs. Have a look at the [Vega Tutorial][7]
for an introduction. In the future we hope to offer a simplified method for creating these charts. 
Perhaps after reading this post you will be inspired to help add such a feature. 

Publishing an Insight
---------------------

The final step after creating and visualizing a query is to publish it for others to see. Simply click the "Publish"
button and we'll add it the Popular Insights page for others to view and make derivatives.


[0]: https://www.evernote.com/shard/s13/sh/3bebb8f8-b9ba-449d-8c34-41a9a24881c8/b63374146f7cdb52811ac63631cedb9a/deep/0/Caravela-Explore%20the%20Web.png "Published Insights Screenshot"

[1]: https://www.evernote.com/shard/s13/sh/74c98cd0-dacd-48f9-9e60-4c96c9fd16f3/04ae3c51eb383cbbbce24dfdca78de25/deep/0/Caravela-Explore%20the%20Web%20and%20Hulu%20-%20Watch%20and%20untitled%20and%201Password.png
 "Insight Screenshot"

[2]: https://www.evernote.com/shard/s13/sh/5ed43278-74c8-4f08-a0f0-94abec337e81/439ef3b64ddb6d61aeb90be721186e98/deep/0/Caravela-Explore%20the%20Web.png "Querying Data"

[3]: https://www.evernote.com/shard/s13/sh/d97eb203-a192-44c6-a6fe-79b184209b51/fa9d71a705327aa161a896a91af6f9a4/deep/0/Caravela-Explore%20the%20Web.png "Exploring Data"

[4]: https://github.com/trivio/splicer

[5]: https://splicer.readthedocs.org/en/latest/ "Splicer API"

[6]: http://trifacta.github.io/vega/ "Trifacta's Visualization Grammar"

[7]: https://github.com/trifacta/vega/wiki/Tutorial "Vega Tutorial"

[8]: http://commoncrawl.org "Common Crawl"

[9]: https://caravela.mozillalabs.com "Caravela"

[10]: https://github.com/mozilla/caravela "Fork Us"

