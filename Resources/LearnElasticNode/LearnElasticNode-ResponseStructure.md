#elastic

```
{
  "took": 30,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "notes",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "title": "Learning Elasticsearch",
          "content": "This is an example note.",
          "tags": ["elasticsearch", "nodejs"]
        }
      },
      {
        "_index": "notes",
        "_id": "2",
        "_score": 0.9,
        "_source": {
          "title": "Node.js with Elasticsearch",
          "content": "Another note on Elasticsearch with Node.js.",
          "tags": ["nodejs", "search"]
        }
      }
    ]
  }
}



```
