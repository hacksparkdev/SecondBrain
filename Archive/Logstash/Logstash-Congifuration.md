#Logstash

To set up the Logstash server after installation, follow these steps to configure it to receive logs from your Python workstations and forward them to Elasticsearch.

### 1. **Configure Logstash**

After installation, you need to configure Logstash with an input (to receive logs from the Python scripts) and an output (to send logs to Elasticsearch).

### Step 1: Create a Logstash Configuration File

1. **Location**: The default location for Logstash configuration files is `/etc/logstash/conf.d/`.
2. **Create a new file**:
    
    ```bash
    sudo nano /etc/logstash/conf.d/logstash.conf
    
    ```
    
3. **Add the following configuration**:
    - This configuration sets up Logstash to:
        - Listen on TCP port `5044` to receive logs from Python.
        - Forward logs to your Elasticsearch instance.
    
    ```
    input {
      tcp {
        port => 5044
        codec => json_lines
      }
    }
    
    filter {
      # Add any filters here if needed, for example:
      # Mutate, date parsing, etc.
    }
    
    output {
      elasticsearch {
        hosts => ["http://<elasticsearch-server-ip>:9200"]
        index => "windows-logs"
      }
    }
    
    ```
    
    - **Input**:
        - `tcp`: Logstash listens on port `5044` for incoming logs.
        - `codec => json_lines`: This ensures Logstash can handle logs sent in JSON format (from your Python script).
    - **Output**:
        - `elasticsearch`: Logstash forwards logs to the Elasticsearch instance at the given IP address (`http://<elasticsearch-server-ip>:9200`).
        - `index => "windows-logs"`: Logs are stored in the `windows-logs` index in Elasticsearch.

### Step 2: Validate the Configuration

After creating the configuration file, it’s a good idea to validate it to make sure there are no syntax errors:

```bash
sudo /usr/share/logstash/bin/logstash --config.test_and_exit -f /etc/logstash/conf.d/logstash.conf

```

This will output any errors in the configuration file if present. If there are no errors, you will see something like:

```
Configuration OK

```

### Step 3: Start the Logstash Service

After validating the configuration, start the Logstash service:

```bash
sudo systemctl start logstash

```

Ensure the service is enabled to start automatically on boot:

```bash
sudo systemctl enable logstash

```

Check the status to ensure it’s running properly:

```bash
sudo systemctl status logstash

```

You should see `active (running)` if Logstash started successfully.

### 2. **Allow Port 5044 (Optional)**

If you have a firewall enabled, allow TCP traffic on port `5044` so that Logstash can receive logs:

```bash
sudo ufw allow 5044/tcp

```

### 3. **Test the Logstash Setup**

Once Logstash is configured and running, test the connection by sending sample logs from your Python script to Logstash.

For example, ensure your Python script (e.g., `client.py`) points to the correct Logstash server IP and port:

```python
LOGSTASH_HOST = 'logstash-server-ip'
LOGSTASH_PORT = 5044

```

Start your Python script and check the Logstash logs to confirm that it is receiving the data:

```bash
sudo journalctl -u logstash

```

### 4. **Verify Log Data in Elasticsearch**

After confirming that Logstash is receiving logs, verify that Elasticsearch is receiving the logs. You can use Elasticsearch’s REST API to search for the logs:

```bash
curl -X GET "http://<elasticsearch-server-ip>:9200/windows-logs/_search?pretty"

```

This will output the logs that have been stored in the `windows-logs` index.

---

### Summary

- You set up a **Logstash configuration file** to listen on port 5044 and forward logs to Elasticsearch.
- Started the Logstash service and allowed traffic through the necessary port.
- Tested that logs are received by Logstash and forwarded to Elasticsearch.

With this, Logstash is now set up to receive logs from your Python scripts and send them to Elasticsearch for storage and analysis.
