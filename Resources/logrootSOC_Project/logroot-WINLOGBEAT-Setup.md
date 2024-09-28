#Winlogbeat #logroot

### **Winlogbeat Tutorial**

**Winlogbeat** is an open-source log shipper from Elastic that collects and sends Windows Event logs to Elasticsearch or Logstash. It's commonly used in Security Information and Event Management (SIEM) systems to collect logs for analysis.

Here’s a step-by-step tutorial to get started with Winlogbeat:

---

### **1. Install Winlogbeat**

### **Step 1: Download Winlogbeat**

1. Go to the [Winlogbeat downloads page](https://www.elastic.co/downloads/beats/winlogbeat).
2. Download the latest version of Winlogbeat for Windows.

### **Step 2: Extract the ZIP File**

1. Extract the downloaded `.zip` file to a directory like `C:\\Program Files\\Winlogbeat`.

---

### **2. Configure Winlogbeat**

### **Step 1: Open the Winlogbeat Configuration File**

The main configuration file is `winlogbeat.yml`. Open this file in a text editor.

### **Step 2: Configure Event Log Inputs**

In the configuration file, you need to specify which Windows event logs you want Winlogbeat to collect.

Here’s an example configuration:

```yaml
winlogbeat.event_logs:
  - name: Application
    ignore_older: 72h
  - name: Security
    ignore_older: 72h
  - name: System
    ignore_older: 72h

```

- **`name`**: The name of the event log to monitor (e.g., `Security`, `Application`, `System`).
- **`ignore_older`**: This skips events that are older than the specified time (in this case, 72 hours).

### **Step 3: Set the Output**

Next, configure where Winlogbeat should send the logs. You can send them directly to **Elasticsearch** or **Logstash**.

**For Elasticsearch Output**:

```yaml
output.elasticsearch:
  hosts: ["<http://localhost:9200>"]

```

**For Logstash Output** (if you want to send logs to Logstash first for further processing):

```yaml
output.logstash:
  hosts: ["localhost:5044"]

```

You can only have one output enabled at a time. If you're using Logstash, comment out the Elasticsearch output and vice versa.

### **Step 4: Setup Elasticsearch Index Management**

Winlogbeat can automatically create the necessary index patterns in Elasticsearch for you. To enable this, add the following settings:

```yaml
setup.template.enabled: true
setup.template.settings:
  index.number_of_shards: 1

```

This will ensure that the appropriate index template is set up in Elasticsearch when Winlogbeat sends data.

---

### **3. Test the Configuration**

Before running Winlogbeat, it’s important to ensure that the configuration is correct. Use the following command to test it:

1. Open a **Command Prompt** as an administrator.
2. Navigate to the Winlogbeat directory:
    
    ```bash
    cd "C:\\Program Files\\Winlogbeat"
    
    ```
    
3. Run the test command:
    
    ```bash
    winlogbeat.exe test config -c winlogbeat.yml -e
    
    ```
    

If the configuration is valid, you will see a confirmation message.

---

### **4. Set Up Dashboards (Optional)**

If you're sending logs to Elasticsearch and using **Kibana**, Winlogbeat can set up pre-built dashboards for you. To do this, add the following line to your configuration file:

```yaml
setup.dashboards.enabled: true

```

Then run:

```bash
winlogbeat.exe setup --dashboards

```

This will load the pre-built dashboards into Kibana so you can visualize your event logs.

---

### **5. Start Winlogbeat**

Once the configuration is set up and tested, you can start Winlogbeat.

### **Step 1: Start Winlogbeat as a Service**

You can run Winlogbeat as a Windows service so it starts automatically on system boot.

To install the service:

```bash
winlogbeat.exe install

```

To start the service:

```bash
Start-Service winlogbeat

```

### **Step 2: Verify Logs in Elasticsearch or Logstash**

After starting Winlogbeat, check if logs are being sent to Elasticsearch or Logstash.

- **For Elasticsearch**: Use Kibana to visualize the logs.
- **For Logstash**: Check Logstash's logs to verify that the logs are being received.

---

### **6. Monitor Winlogbeat Logs**

If there are any issues or you need to troubleshoot, you can view Winlogbeat’s logs, which are stored in:

```
C:\\ProgramData\\Winlogbeat\\Logs\\

```

Check this directory for any errors or issues related to log collection or transmission.

---

### **7. Stopping and Removing Winlogbeat**

To stop Winlogbeat as a service:

```bash
Stop-Service winlogbeat

```

To uninstall the service:

```bash
winlogbeat.exe uninstall

```

---

### **8. Advanced Configurations**

### **Filtering Events**

You can filter events based on specific conditions (like event IDs) before sending them to Elasticsearch or Logstash.

```yaml
winlogbeat.event_logs:
  - name: Security
    event_id: 4624, 4625

```

This will only send logon and logoff events (event IDs 4624 and 4625) from the Security log.

### **Configure Fields**

You can add custom fields to each event for better filtering in Elasticsearch:

```yaml
fields:
  environment: production
  department: IT

```

---

### **Conclusion**

- **Winlogbeat** is an efficient and easy-to-use log shipper for Windows Event Logs, providing real-time visibility into your logs.
- Use the appropriate configuration to filter logs, choose output destinations, and set up dashboards for analysis.
- It integrates seamlessly with **Elasticsearch** and **Kibana**, making it a great tool for Windows event monitoring in SOC environments.

By following these steps, you’ll have a functional setup that can ship Windows Event Logs to Elasticsearch or Logstash, where you can visualize, analyze, and set up alerts based on those logs.
