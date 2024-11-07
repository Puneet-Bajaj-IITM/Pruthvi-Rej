# Server Setup Guide for Pruthvi-Rej (Main Branch)

Follow the steps below to set up the server and run the Flask app from the `main` branch.

### 1. **SSH into the Server**
First, SSH into your server using the following command. Make sure you have the SSH private key (`ml-models-ssh-key.pem`) in your local machine.

```bash
ssh -i "ml-models-ssh-key.pem" ubuntu@3.111.123.90
```

### 2. **Clone the Repository**
If you haven't already cloned the repository, clone it from GitHub.

```bash
mkdir flask_app
cd flask_app
git clone https://github.com/Puneet-Bajaj-IITM/Pruthvi-Rej.git
```

### 3. **Navigate to the Project Folder**
Change to the project directory.

```bash
cd Pruthvi-Rej
```

### 4. **Checkout the Main Branch**
Switch to the `main` branch and pull the latest changes from the remote repository.

```bash
git checkout main
git pull origin main
```

### 5. **Update Package Lists**
Update the server's package lists to ensure you have the latest updates.

```bash
sudo apt update
```

### 6. **Install Python 3 Virtual Environment**
Install the required package to create a Python virtual environment.

```bash
sudo apt install python3-venv
```

### 7. **Set Up the Virtual Environment**
Create a virtual environment named `flask_app` and activate it.

```bash
python3 -m venv flask_app
source ./flask_app/bin/activate
```

### 8. **Install Project Dependencies**
Install the required Python dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 9. **Run the Flask App**
Run the Flask app using the following command. Make sure Flask is installed in your environment as a dependency in `requirements.txt`.

```bash
python flask_app.py
```

This will start the Flask server. You can access it on `http://<server-ip>:5000` (replace `<server-ip>` with your VM's IP address).

---

### Notes:
- Ensure port 5000 is open in your firewall or security group settings to allow external access.
- If you encounter any errors related to missing dependencies or configurations, verify that all requirements are correctly installed.
