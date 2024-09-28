#logroot

To package your **Python workers** alongside **Winlogbeat** and create a seamless installation for users, you'll want to bundle everything in a way that allows easy configuration and execution. This will also ensure that the worker runs as a service in the background. Here’s a step-by-step guide on how you can achieve this:

### **Step-by-Step Guide to Packaging Python Workers with Winlogbeat**

---

### **1. Packaging Python Workers and Winlogbeat**

### **1.1. Create a Folder Structure for the Package**

This structure should include everything users need to run your Python worker and Winlogbeat together.

```
/worker-package
│
├── /winlogbeat              # Winlogbeat binary and configurations
│   ├── winlogbeat.exe       # Winlogbeat executable for Windows
│   └── winlogbeat.yml       # Configuration for which event logs to collect (customizable)
│
├── /python-worker           # Python worker code
│   ├── worker.py            # Python worker script for event log processing and module execution
│   ├── config.ini           # Configuration file for the worker (modules, event logs, etc.)
│   ├── /modules             # Custom user-defined Python modules
│   │   └── example_module.py
│   └── requirements.txt     # Python dependencies for the worker
│
└── install.ps1              # PowerShell script to automate installation and service setup

```

---

### **2. Configuration Files**

### **2.1. Winlogbeat Configuration (`winlogbeat.yml`)**

This file will be used to collect specific logs (Security, Application, System, Sysmon, etc.) from the Windows Event Log and send them to your Logstash or Elasticsearch instance.

Key sections of `winlogbeat.yml` that you can allow the user to customize include:

- **Event logs**: Define which event logs to collect (e.g., Security, Sysmon).
- **Output**: Configure where the logs should be sent (e.g., Logstash, Elasticsearch).

Example snippet:

```yaml
winlogbeat.event_logs:
  - name: Security
    ignore_older: 72h
  - name: Sysmon
    ignore_older: 72h

output.elasticsearch:
  hosts: ["<http://your-elasticsearch-server:9200>"]

```

### **2.2. Python Worker Configuration (`config.ini`)**

Allow the user to specify which modules to run, how frequently the worker should poll for tasks, and other settings (e.g., Elasticsearch endpoint, logging preferences).

Example snippet:

```
[worker]
poll_interval = 5  # seconds
elasticsearch_host = <http://your-elasticsearch-server:9200>
logstash_host = <http://your-logstash-server:5044>

[modules]
enabled_modules = example_module  # List of enabled Python modules

[event_logs]
log_types = Security, Sysmon  # Define which logs to collect

[service]
run_as_service = True  # Whether the worker should run as a background service

```

---

### **3. Installation Script**

Write a **PowerShell installation script** (`install.ps1`) that:

1. Installs **Python** (if not already installed).
2. Installs the **required Python dependencies** using `pip` from `requirements.txt`.
3. Sets up **Winlogbeat** as a service.
4. Configures and installs the **Python worker** to run as a Windows service using **nssm** (Non-Sucking Service Manager) or a similar tool.

### **Example PowerShell Script (`install.ps1`)**

```powershell
# Check if Python is installed, if not install it
$python = Get-Command python -ErrorAction SilentlyContinue
if (!$python) {
    Write-Host "Installing Python..."
    Start-Process msiexec.exe -Wait -ArgumentList '/i python-installer.msi /quiet'
}

# Install Python dependencies
Write-Host "Installing Python dependencies..."
Start-Process python -ArgumentList "-m pip install -r ./python-worker/requirements.txt" -Wait

# Install and configure Winlogbeat
Write-Host "Configuring Winlogbeat..."
Start-Process winlogbeat.exe -ArgumentList "install"

# Set up the Python worker as a service using nssm
$nssm_path = "C:\\path\\to\\nssm.exe"
$nssm_install = "$nssm_path install PythonWorker python C:\\path\\to\\python.exe C:\\path\\to\\python-worker\\worker.py"
Start-Process -FilePath $nssm_install -Wait

# Start both services
Start-Service -Name "Winlogbeat"
Start-Service -Name "PythonWorker"

Write-Host "Installation complete. The worker and Winlogbeat are now running as services."

```

### **4. Running the Python Worker as a Service**

### **4.1. Use NSSM to Run Python Worker as a Service**

To ensure the Python worker runs as a background service, you can use a tool like **NSSM (Non-Sucking Service Manager)**, which makes it easy to convert a Python script into a Windows service.

1. Download **nssm** from [here](https://nssm.cc/download).
2. In the PowerShell script, use NSSM to install the worker as a service:
    
    ```bash
    nssm install PythonWorker C:\\path\\to\\python.exe C:\\path\\to\\python-worker\\worker.py
    
    ```
    
3. Configure NSSM to start the service at boot and automatically restart the worker in case of failure:
    
    ```bash
    nssm set PythonWorker Start SERVICE_AUTO_START
    
    ```
    

---

### **5. Distribution and Packaging**

Once everything is set up, you’ll want to bundle the Python worker, Winlogbeat, and the PowerShell installer into a **single zip or installer** that users can easily download.

- **Zip Packaging**: You can package the entire `worker-package` folder into a `.zip` file and include instructions for running the PowerShell script to install the service.
- **Installer**: Alternatively, you can create an installer using tools like **Inno Setup** or **NSIS** to guide users through the installation process, automatically setting up the Python worker and Winlogbeat as services.

---

### **6. Configuration Flexibility for Users**

- **Modules**: Allow users to add or remove Python modules by simply dropping their scripts into the `/modules` folder.
- **Logs to Collect**: They can configure which logs (e.g., Security, Sysmon) to monitor by editing the `config.ini` file and/or `winlogbeat.yml`.
- **Alerting**: Add configuration options for custom alerts, allowing users to specify triggers in `config.ini` that the Python worker should monitor.

---

### **7. Sysmon Integration**

If you plan to include **Sysmon** for more advanced monitoring (e.g., tracking process creation, network connections, etc.), provide a **pre-configured Sysmon XML file** as part of your package.

1. **Install Sysmon** on the user's machine using the PowerShell script:
    
    ```powershell
    Start-Process sysmon.exe -ArgumentList "-accepteula -i sysmon-config.xml" -Wait
    
    ```
    
2. Configure **Winlogbeat** to collect **Sysmon logs** alongside other Windows Event Logs by adding them to the `winlogbeat.yml`:
    
    ```yaml
    - name: Microsoft-Windows-Sysmon/Operational
    
    ```
    

---

### **8. Summary of Flow**

1. **User Downloads the Package**: They download the zip or installer that includes the Python worker, Winlogbeat, and a PowerShell installation script.
2. **User Configures the Package**: They modify the `config.ini` and `winlogbeat.yml` files to specify which logs to collect and which modules to run.
3. **Installation**: They run the **PowerShell script** to install both Winlogbeat and the Python worker as background services.
4. **Logs and Module Results**: The **Python worker** collects logs (e.g., Security, Sysmon), runs custom modules, and sends the data to **Logstash** or **Elasticsearch** for processing and visualization on the central dashboard.
5. **Modular Execution**: The user can easily add new Python modules or modify the configuration without reinstallation.

---

### **Final Thoughts**

By packaging the Python worker with Winlogbeat and making it easy to configure and run as a service, you create a powerful and flexible solution for monitoring Windows Event Logs, running custom Python modules, and sending data to Logstash/Elasticsearch. This setup allows users to easily configure what they want to monitor and ensures the worker runs automatically as a background service without manual intervention.
