#ElasticSearch

Certainly! Below is a detailed tutorial on how to get started with **Elasticsearch**, from installing and setting it up to storing, querying, and analyzing data. This will help you understand how Elasticsearch works and how to apply it effectively in your project.

---

## **Elasticsearch Tutorial**

### 1. **What is Elasticsearch?**

Elasticsearch is a distributed search and analytics engine that allows you to store, search, and analyze large volumes of data in near real-time. It’s commonly used for log and event data, as well as full-text search.

---

### 2. **Installation and Setup**

### **Installing Elasticsearch on Linux/MacOS**

1. **Download Elasticsearch**:
    
    ```bash
    wget <https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.3-linux-x86_64.tar.gz>
    tar -xzf elasticsearch-7.17.3-linux-x86_64.tar.gz
    cd elasticsearch-7.17.3
    
    ```
    
2. **Start Elasticsearch**:
    
    ```bash
    ./bin/elasticsearch
    
    ```
    
    Elasticsearch will now start and listen on port `9200` by default.
    

### **Installing Elasticsearch on Windows**

1. **Download the ZIP file** from the [Elasticsearch website](https://www.elastic.co/downloads/elasticsearch).
2. **Unzip the folder** and navigate to the `bin` directory.
3. **Run the following command**:
    
    ```bash
    elasticsearch.bat
    
    ```
    

### **Testing Elasticsearch**

After starting Elasticsearch, you can test if it's running by making a request to `http://localhost:9200`.

```bash
curl <http://localhost:9200>
Curl POST request
curl -X POST http://10.10.20.100:3000/trigger-python-module -H "Content-Type: application/json" -d '{"moduleName": "log_collector"}'

​
To query Elasticsearch and see what's in it from the terminal, you can use curl or http commands to interact with the Elasticsearch REST API. Here's a basic guide:
Prerequisites:
Ensure Elasticsearch is running and accessible from your terminal.
curl should be installed on your machine.
Basic Commands:
Check Elasticsearch Health:
curl -X GET "localhost:9200/_cluster/health?pretty"

​
This command provides the health status of your Elasticsearch cluster.
List All Indices:
curl -X GET "localhost:9200/_cat/indices?v"

​
This command lists all indices in your Elasticsearch cluster along with their status.
Query a Specific Index:
To search within a specific index, use the following command:
curl -X GET "localhost:9200/index_name/_search?pretty"

​
Replace index_name with the name of the index you want to query. This will return the documents in that index.
Run a Search Query:
You can use a more specific search query to filter the results:
curl -X GET "localhost:9200/index_name/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "field_name": "search_value"
    }
  }
}
'

​
Replace index_name, field_name, and search_value with your index name, field, and the value you're searching for, respectively.
View Cluster Stats:
curl -X GET "localhost:9200/_cluster/stats?pretty"

​
Delete Index
curl -X DELETE "http://localhost:9200/index_name"

​
Create Index 
curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
'
​
Explanation:
X GET specifies the HTTP method to use.
localhost:9200 is the default address for an Elasticsearch instance running on your local machine. Adjust it if your Elasticsearch instance is running on a different host or port.
?pretty makes the output more readable.
These commands should give you a good starting point for querying and exploring the data in your Elasticsearch instance.
```

You should see a response with Elasticsearch version details.

---

### 3. **Basic Concepts**

### **Index**

An index in Elasticsearch is similar to a database in SQL. You store your data in indexes, which are essentially collections of documents.

### **Document**

A document is the basic unit of information stored in Elasticsearch. It's similar to a row in a SQL database, but it’s stored in JSON format.

### **Mapping**

Mapping defines how the data fields are stored and indexed in Elasticsearch. You specify field types (e.g., `text`, `keyword`, `date`, etc.) in mappings.

---

### 4. **Creating an Index and Adding Data**

### **Create an Index**

You can create an index by sending a `PUT` request to Elasticsearch:

```bash
curl -X PUT "localhost:9200/my_index"

```

This will create an empty index called `my_index`.

### **Inserting a Document**

Insert a document into the index with a `POST` request:

```bash
curl -X POST "localhost:9200/my_index/_doc/1" -H 'Content-Type: application/json' -d'
{
  "name": "John Doe",
  "age": 30,
  "message": "Elasticsearch tutorial"
}'

```

This inserts a document with ID `1` into the `my_index` index.

### **Viewing a Document**

You can retrieve the document using its ID:

```bash
curl -X GET "localhost:9200/my_index/_doc/1"

```

### **Delete a Document**

To delete a document, use the `DELETE` request:

```bash
curl -X DELETE "localhost:9200/my_index/_doc/1"

```

---

### 5. **Index Mappings**

By default, Elasticsearch will dynamically create mappings for fields when you insert documents. However, it's better to explicitly define mappings for fields that you'll frequently search or aggregate.

### **Creating an Index with Explicit Mappings**

```bash
curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "age": { "type": "integer" },
      "timestamp": { "type": "date" },
      "message": { "type": "text" }
    }
  }
}'

```

This command creates an index with fields `name` and `message` as `text` (for full-text search), `age` as an `integer`, and `timestamp` as a `date` field.

---

### 6. **Searching Data**

Elasticsearch provides powerful search capabilities. Here’s how you can search for documents:

### **Basic Search**

```bash
curl -X GET "localhost:9200/my_index/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "message": "tutorial"
    }
  }
}'

```

This searches for documents in the `my_index` index where the `message` field contains the word “tutorial.”

### **Filtering Results**

You can add filters to limit the results:

```bash
curl -X GET "localhost:9200/my_index/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": {
        "match": { "message": "tutorial" }
      },
      "filter": {
        "range": {
          "age": {
            "gte": 25
          }
        }
      }
    }
  }
}'

```

This query searches for documents where the `message` field matches "tutorial" and the `age` is greater than or equal to 25.

---

### 7. **Aggregations**

Aggregations are used to analyze your data by summarizing it.

### **Counting Documents**

To count the number of documents:

```bash
curl -X GET "localhost:9200/my_index/_count"

```

### **Term Aggregation**

You can group documents by a field. For example, to find how many documents contain each value in the `age` field:

```bash
curl -X GET "localhost:9200/my_index/_search" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "ages": {
      "terms": { "field": "age" }
    }
  }
}'

```

---

### 8. **Index Lifecycle Management (ILM)**

Elasticsearch offers **Index Lifecycle Management (ILM)** to manage the lifecycle of your data. This is useful for log and event data, where you may want to archive or delete old indices automatically.

### **Creating an ILM Policy**

```bash
curl -X PUT "localhost:9200/_ilm/policy/my_policy" -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "30d"
          }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}'

```

This policy will:

- Rollover to a new index every 50GB or 30 days.
- Delete data after 90 days.

### **Applying the ILM Policy**

To apply the policy to an index, use the following command:

```bash
curl -X PUT "localhost:9200/my_index/_settings" -H 'Content-Type: application/json' -d'
{
  "index.lifecycle.name": "my_policy"
}'

```

---

### 9. **Index Templates**

Index templates allow you to apply settings and mappings automatically when a new index is created. This is particularly useful for time-based indices (e.g., logs-2024-09-19).

### **Create an Index Template**

```bash
curl -X PUT "localhost:9200/_template/logs_template" -H 'Content-Type: application/json' -d'
{
  "index_patterns": ["logs-*"],
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "hostname": { "type": "keyword" },
      "moduleName": { "type": "keyword" },
      "status": { "type": "keyword" },
      "message": { "type": "text" }
    }
  }
}'

```

This template will apply to any index that matches the pattern `logs-*`.

---

### 10. **Handling Time-Based Data**

For logging or monitoring use cases, store logs in time-based indices (e.g., `logs-2024-09-19`) and use index lifecycle management (ILM) to automatically manage old data.

### **Best Practices for Time-Based Indices**

- Use an index pattern like `logs-YYYY-MM-DD`.
- Apply mappings and templates to ensure consistent data structure.
- Use ILM to handle old data.

---

### Conclusion

By following this tutorial, you now know how to:

- Install Elasticsearch.
- Create indices and mappings.
- Insert, query, and search data.
- Perform aggregations for analytics.
- Implement ILM for data retention.
- Use templates for managing time-based indices.

Elasticsearch is a powerful tool for log management, real-time data analytics, and search use cases. You can now apply these concepts to your current project to store and retrieve data efficiently.
