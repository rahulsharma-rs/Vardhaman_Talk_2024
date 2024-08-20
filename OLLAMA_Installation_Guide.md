
# On-Prem OLLAMA Installation with Open WebUI Chat Utility

## Pre-requisites
Ensure you have a virtual machine running with appropriate resources allocated and access to the internet.

## Step 1: Install Apache2 Web Server
1. **Update your package manager**:
   ```bash
   sudo apt-get update
   ```

2. **Install Apache2**:
   ```bash
   sudo apt-get install apache2
   ```

## Step 2: Configure Apache2 as a Reverse Proxy
1. **Enable necessary Apache modules**:
   ```bash
   sudo a2enmod proxy proxy_http proxy_balancer lbmethod_byrequests
   ```

2. **Restart Apache to apply the changes**:
   ```bash
   sudo systemctl restart apache2
   ```

3. **Create a reverse proxy configuration file**:
   ```bash
   sudo nano /etc/apache2/sites-available/open-webui.conf
   ```

   Add the following to the configuration file:
   ```apache
   <VirtualHost *:80>
       ServerName yourdomain.com
       ServerAdmin your-email@domain.com
       ProxyPass / http://127.0.0.1:8080/
       ProxyPassReverse /app http://127.0.0.1:8080/
       ErrorLog ${APACHE_LOG_DIR}/error.log
       LogLevel warn
       CustomLog ${APACHE_LOG_DIR}/access.log combined
   </VirtualHost>
   ```

4. **Enable the new site configuration**:
   ```bash
   sudo a2ensite open-webui.conf
   sudo a2dissite 000-default.conf
   ```

5. **Restart Apache to activate the new configuration**:
   ```bash
   sudo systemctl restart apache2
   ```

6. **Adjust firewall settings (if necessary)** to allow HTTP traffic on port 80:
   ```bash
   sudo ufw allow 80
   ```

7. **Test the setup** by accessing your application via http://yourdomain.com or the server's IP.

## Step 3: Install Docker
1. **Set up Docker's repository**:
   ```bash
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update
   ```

2. **Install Docker**:
   ```bash
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

3. **Verify Docker installation**:
   ```bash
   sudo docker run hello-world
   ```

## Step 4: Install OLLAMA Language Model
1. **Download and install OLLAMA**:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Run the OLLAMA model**:
   ```bash
   ollama run llama3:8b
   ```

3. **Test the OLLAMA model**:
   ```bash
   curl http://localhost:11434/api/generate -d '{
       "model": "llama3:8b",
       "prompt": "Why is the sky blue?",
       "stream": false
   }'

   curl http://localhost:11434/api/generate -d '{
       "model": "llama3:8b",
       "prompt": "Give me a python code for factorial of a number",
       "stream": false
   }'
   ```

## Step 5: Install OpenWebUI
1. **Deploy OpenWebUI using Docker**:
   ```bash
   docker run -d --network=host -v /home/ubuntu:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
   ```

## Completion
Your setup should now be complete, and you can access the OpenWebUI to interact with the OLLAMA model via a web interface. Make sure to replace "yourdomain.com" and other placeholders with the actual values specific to your setup.
