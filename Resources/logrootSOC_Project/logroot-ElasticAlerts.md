#logroot

Since you already have **Elasticsearch** and **Winlogbeat** set up, we can focus on configuring alerts in Elasticsearch using **Watcher** or **ElastAlert**. Below are the steps to set up alerts:

### Step-by-Step Guide to Set Up Alerts

### **Option 1: Using Elasticsearch Watcher**

Elasticsearch Watcher is a powerful alerting engine built into the **X-Pack** feature of Elasticsearch. Here's how to set it up:

### **Step 1: Enable Watcher (if not enabled)**

Watcher is part of **Elastic Stack’s** X-Pack features, so ensure it is enabled on your Elasticsearch instance.

```bash
curl -X POST "localhost:9200/_watcher/_start"

```

### **Step 2: Create a Basic Watch for Failed Logins**

You’ll now create a watch that monitors your logs and sends an alert when a certain condition (like multiple failed login attempts) is met.

Example: Alert if there are more than 5 failed login attempts within a 10-minute window.

1. **Define the Watch**:
    - Open **Kibana** or use **cURL** and create a watch in the `/_watcher/watch/` endpoint.
    - This example creates a watch that monitors login failure events.

```bash
PUT _watcher/watch/failed_login_alert
{
  "trigger": {
    "schedule": { "interval": "10m" }   // Check every 10 minutes
  },
  "input": {
    "search": {
      "request": {
        "indices": ["winlogbeat-*"],  // Index pattern
        "body": {
          "query": {
            "bool": {
              "must": [
                { "match": { "event.action": "failed_login" } },   // Match failed login events
                { "range": { "@timestamp": { "gte": "now-10m/m", "lte": "now" } } }  // Last 10 mins
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": {
      "ctx.payload.hits.total.value": { "gte": 5 }   // Trigger if there are 5 or more events
    }
  },
  "actions": {
    "email_admin": {
      "email": {
        "to": "admin@example.com",
        "subject": "Failed Login Alert",
        "body": "More than 5 failed login attempts detected in the last 10 minutes."
      }
    }
  }
}

```

1. **Start the Watch**:
Once the watch is created, Elasticsearch Watcher will start monitoring the logs and trigger an alert based on the defined criteria.
2. **Test the Watch**:
    - You can manually execute the watch to see if it's working:
    
    ```bash
    POST _watcher/watch/failed_login_alert/_execute
    
    ```
    

### **Step 3: Modify the Watch to Trigger Different Actions**

You can modify the action to trigger other alerts such as Slack messages, webhook notifications, or sending tasks to analysts.

Example of triggering a webhook instead of an email:

```json
"actions": {
  "webhook_alert": {
    "webhook": {
      "method": "POST",
      "url": "<http://your-node-server/api/alert>",
      "body": {
        "alert": "Failed logins detected",
        "count": "{{ctx.payload.hits.total.value}}"
      }
    }
  }
}

```

---

### **Option 2: Using ElastAlert**

**ElastAlert** is an open-source alternative to Watcher, useful for more flexible alerting without X-Pack.

### **Step 1: Install ElastAlert**

1. Install ElastAlert:
    
    ```bash
    git clone <https://github.com/Yelp/elastalert.git>
    cd elastalert
    sudo python setup.py install
    
    ```
    
2. Install the required dependencies:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    

### **Step 2: Configure ElastAlert**

1. Create a configuration file (`config.yaml`) for ElastAlert:
    
    ```yaml
    es_host: localhost
    es_port: 9200
    writeback_index: elastalert_status  # Index to store ElastAlert status
    buffer_time:
      minutes: 15  # Time to buffer logs
    
    ```
    
2. Create an alert rule file (`rule.yaml`), which defines the criteria for triggering an alert. Here's an example to detect failed login attempts:

```yaml
name: Failed Login Alert
type: frequency
index: winlogbeat-*  # Match your index pattern
num_events: 5  # Trigger if more than 5 failed logins
timeframe:
  minutes: 10  # Within a 10-minute window
filter:
- term:
    event.action: "failed_login"  # Filter for failed login events
alert:
- "email"
email:
- "admin@example.com"

```

1. **Test the Rule**:
Test the rule configuration using:
    
    ```bash
    elastalert-test-rule rule.yaml
    
    ```
    

### **Step 3: Run ElastAlert**

Start ElastAlert, and it will continuously monitor the logs based on your rules:

```bash
elastalert --config config.yaml

```

---

### **Step 4: Display Alerts in Your Node.js Interface**

Once alerts are triggered (whether using Watcher or ElastAlert), you need to display them in your Node.js dashboard.

1. **Create an API Endpoint for Alerts**:
    - If you are using webhooks (from Watcher or ElastAlert), create an API endpoint in your Node.js app that receives alert data.

```jsx
app.post('/api/alert', (req, res) => {
  const alertData = req.body;

  // Save alert to your database or send it to analysts
  console.log("Alert Received:", alertData);

  res.status(200).json({ message: 'Alert received' });
});

```

1. **Display Alerts in the Dashboard**:
    - Fetch alerts from your database (or from Elasticsearch) and display them on the analyst’s dashboard.
    - Use **EJS** or another front-end tool to show alerts in real time.

```
<h1>Alerts</h1>
<table>
  <thead>
    <tr>
      <th>Alert</th>
      <th>Type</th>
      <th>Timestamp</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <% alerts.forEach(alert => { %>
      <tr>
        <td><%= alert.title %></td>
        <td><%= alert.type %></td>
        <td><%= new Date(alert.timestamp).toLocaleString() %></td>
        <td><%= alert.status %></td>
      </tr>
    <% }) %>
  </tbody>
</table>

```

### Conclusion

- Use **Elasticsearch Watcher** or **ElastAlert** to monitor logs for specific conditions and trigger alerts.
- Alerts can be routed via email, webhooks, or directly to a dashboard in your **Node.js** app.
- Customize the alerting conditions (e.g., failed logins, CPU usage) and actions (e.g., sending emails, triggering tasks).

Would you like further assistance with configuring specific alert actions or customizing the alert interface?
