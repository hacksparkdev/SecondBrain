#logroot


In the context of being a **SOC analyst**, enriching data in Logstash allows you to **add context** to raw logs by appending additional information, such as threat intelligence, geographical location, or custom metadata. This enrichment process enables you to **correlate security events**, **detect threats**, and **act on indicators of compromise (IOCs)** more effectively.

In this explanation, I'll walk you through how to **enrich log data using Logstash**, with a specific focus on **threat intelligence enrichment using MISP**.

---

## **1. Overview: Why Enrich Data in Logstash?**

In SOC operations, logs by themselves may lack enough information to make meaningful decisions. For example, a log showing a failed login attempt from a particular IP address may be more significant if that IP is known to be associated with a threat actor or malware campaign.

**Enrichment** in Logstash enables you to:

- **Correlate security events with external data** (like threat intelligence feeds).
- **Add more context to your logs**, such as geographical location, reputation, or known malicious indicators.
- **Enhance detection** by flagging logs containing known IOCs (IPs, hashes, domains) from threat intelligence sources.

---

## **2. What is MISP?**

**MISP (Malware Information Sharing Platform)** is an open-source platform that **collects, stores, and shares threat intelligence**. MISP can provide you with information about:

- **Malicious IP addresses**.
- **Domains associated with malware**.
- **File hashes (MD5, SHA1, SHA256)** of known malware samples.
- **Threat actors and campaign details**.

By integrating MISP with Logstash, you can **enrich incoming logs** with threat intelligence data, helping you detect security events related to known threats.

---

## **3. How Does Data Enrichment in Logstash Work?**

To enrich data in Logstash, the general process is:

1. **Ingest log data** (e.g., from Winlogbeat, Syslog, or other sources).
2. **Use filters** to modify or enrich the data (e.g., adding threat intelligence data).
3. **Output enriched data** to Elasticsearch for further analysis and alerting.

---

## **4. Steps to Enrich Data in Logstash with MISP**

### **Step 1: Set Up MISP Threat Intelligence Integration**

1. **MISP Threat Intelligence Feed**: First, you need access to a MISP instance that provides threat intelligence feeds. This could be an internal instance or a public MISP server.
2. **Export MISP Data**: Export threat intelligence data from MISP, including:
    - **IP addresses** of known bad actors.
    - **Domains** associated with phishing or malware.
    - **File hashes** of known malicious files.
    
    This can be done via **MISP’s REST API** or by downloading CSV/JSON files containing the IOCs.
    

### **Step 2: Load MISP Data into Logstash**

To enrich logs with MISP threat intelligence, you can:

- Use **static enrichment** (loading MISP data as a file into Logstash).
- Use **dynamic enrichment** (querying the MISP API during Logstash processing).

### **Option A: Static Enrichment (File-based)**

1. **Export MISP data** to a CSV, JSON, or YAML file.
2. **Load the MISP data** into Logstash using the `translate` or `csv` filter.

Example configuration for file-based enrichment:

```yaml
filter {
  csv {
    path => "/path/to/misp_iocs.csv"
    columns => ["ioc_type", "ioc_value", "threat_level", "description"]
    separator => ","
  }

  if [source_ip] {
    translate {
      field => "[source_ip]"
      destination => "[ioc_info]"
      dictionary_path => "/path/to/ip_mappings.yaml"
      fallback => "unknown"
    }
  }
}

```

In this example:

- **MISP data** is stored in a file (e.g., a CSV of malicious IP addresses).
- **Translate filter** checks if the incoming log's `source_ip` matches an IOC in the file and adds additional fields like `threat_level` and `description`.

### **Option B: Dynamic Enrichment (MISP API)**

1. Use Logstash's **http filter** to query the **MISP API** dynamically as logs are processed. This is ideal for enriching logs with up-to-date threat intelligence.

Example configuration for querying the MISP API:

```yaml
filter {
  http {
    url => "<https://your-misp-instance/api/attributes/restSearch/json>"
    query => {
      "value" => "%{[source_ip]}"
    }
    headers => {
      "Authorization" => "YOUR_MISP_API_KEY"
    }
    target_body => "misp_response"
  }

  if [misp_response][Attribute] {
    mutate {
      add_field => {
        "threat_level" => "%{[misp_response][Attribute][threat_level]}"
        "ioc_description" => "%{[misp_response][Attribute][description]}"
      }
    }
  }
}

```

In this example:

- Logstash makes an HTTP request to MISP’s API for each log's `source_ip`.
- If the IP matches an IOC, Logstash enriches the log with the corresponding `threat_level` and `ioc_description`.

### **Step 3: Processing and Filtering the Logs**

Once the log data is enriched, you can filter and process the logs further based on the threat intelligence information. For instance, you can:

- Flag logs where the `threat_level` is **high**.
- Alert when a known **malicious IP address** is detected in the logs.
- Filter out logs that are not related to known IOCs to reduce data volume.

Example filter configuration:

```yaml
filter {
  if [threat_level] == "high" {
    mutate {
      add_tag => [ "alert", "critical_threat" ]
    }
  }
}

```

This configuration flags any log with a high threat level, allowing you to trigger alerts or actions.

---

## **5. Sending Enriched Data to Elasticsearch**

After enrichment, the logs are ready to be sent to **Elasticsearch**. Elasticsearch will index the logs, allowing you to query and visualize them in tools like **Kibana**.

### Example output configuration for Elasticsearch:

```yaml
output {
  elasticsearch {
    hosts => ["<http://localhost:9200>"]
    index => "enriched-logs-%{+YYYY.MM.dd}"
    document_id => "%{[@metadata][id]}"
  }
}

```

The enriched logs will be sent to an index named `enriched-logs-YYYY.MM.dd`, where each log includes:

- The original fields (e.g., `source_ip`, `timestamp`).
- Enriched fields from MISP (e.g., `threat_level`, `ioc_description`).

---

## **6. Benefits of Enrichment for SOC Analysts**

**Real-time Threat Detection**:

- By enriching logs with MISP IOCs, you can detect real-time threats, such as connections to known bad IPs or domains.

**Prioritization**:

- Enrichment allows SOC analysts to prioritize incidents based on the **severity** of the threat, e.g., immediately alerting on logs with high-risk IOCs.

**Threat Hunting**:

- Enriched logs allow analysts to **search and filter** based on enriched fields like `threat_level` or `ioc_description`,
