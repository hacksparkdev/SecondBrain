#ElasticSearch

Curl POST request

```jsx
curl -X POST http://10.10.20.100:3000/trigger-python-module -H "Content-Type: application/json" -d '{"moduleName": "log_collector"}'

```

To query Elasticsearch and see what's in it from the terminal, you can use `curl` or `http` commands to interact with the Elasticsearch REST API. Here's a basic guide:

### Prerequisites:

- Ensure Elasticsearch is running and accessible from your terminal.
- `curl` should be installed on your machine.

### Basic Commands:

1. **Check Elasticsearch Health:**
    
    ```bash
    curl -X GET "localhost:9200/_cluster/health?pretty"
    
    ```
    
    This command provides the health status of your Elasticsearch cluster.
    
2. **List All Indices:**
    
    ```bash
    curl -X GET "localhost:9200/_cat/indices?v"
    
    ```
    
    This command lists all indices in your Elasticsearch cluster along with their status.
    
3. **Query a Specific Index:**
To search within a specific index, use the following command:
    
    ```bash
    curl -X GET "localhost:9200/index_name/_search?pretty"
    
    ```
    
    Replace `index_name` with the name of the index you want to query. This will return the documents in that index.
    
4. **Run a Search Query:**
You can use a more specific search query to filter the results:
    
    ```bash
    curl -X GET "localhost:9200/index_name/_search?pretty" -H 'Content-Type: application/json' -d'
    {
      "query": {
        "match": {
          "field_name": "search_value"
        }
      }
    }
    '
    
    ```
    
    Replace `index_name`, `field_name`, and `search_value` with your index name, field, and the value you're searching for, respectively.
    
5. **View Cluster Stats:**
    
    ```bash
    curl -X GET "localhost:9200/_cluster/stats?pretty"
    
    ```
    

### Delete Index

```bash
curl -X DELETE "http://localhost:9200/index_name"

```

### Create Index

```bash
curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
'
```

### Explanation:

- `X GET` specifies the HTTP method to use.
- `localhost:9200` is the default address for an Elasticsearch instance running on your local machine. Adjust it if your Elasticsearch instance is running on a different host or port.
- `?pretty` makes the output more readable.

These commands should give you a good starting point for querying and exploring the data in your Elasticsearch instance.
