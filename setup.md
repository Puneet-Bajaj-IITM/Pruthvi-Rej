Here's a `setup.md` file that your client can follow to set up the environment on their server. This includes all the necessary commands for cloning your repository, setting up the virtual environment, installing dependencies, and running the app.

---

# Server Setup Guide for Pruthvi-Rej

Follow the steps below to set up the server and run the Pruthvi-Rej project.

### 1. **SSH into the Server**
First, SSH into your server using the following command. Make sure you have the SSH private key (`ml-models-ssh-key.pem`) in your local machine.

```bash
ssh -i "ml-models-ssh-key.pem" ubuntu@3.111.123.90
```

### 2. **Clone the Repository**
Clone the project repository from GitHub.

```bash
mkdir runway
git clone https://github.com/Puneet-Bajaj-IITM/Pruthvi-Rej.git
```

### 3. **Navigate to the Project Folder**
Change to the project directory.

```bash
cd runway/Pruthvi-Rej
```

### 4. **Create and Checkout a New Branch**
Create a new branch named `runway` and pull the latest changes from the remote repository.

```bash
git checkout -b runway
git pull origin runway
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
Create a virtual environment named `runway` and activate it.

```bash
python3 -m venv runway
source ./runway/bin/activate
```

### 8. **Install Project Dependencies**
Install the required Python dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 9. **Install Ollama**
Install Ollama for running large language models locally.

```bash
curl https://ollama.ai/install.sh | sh
```

### 10. **Start Ollama Server**
Run Ollama in the background.

```bash
nohup ollama serve &
```

### 11. **Install Additional System Utilities**
Install some additional system utilities required for hardware information and optimizations.

```bash
sudo apt update
sudo apt install pciutils lshw
```

### 12. **Pull the Model**
Pull the `llama3.1` model from Ollama.

```bash
ollama pull llama3.1
```

### 13. **Start a tmux Session**
Start a `tmux` session to keep your environment persistent.

```bash
tmux new-session -s runway
```

If you're already inside a tmux session, you can attach to it with:

```bash
tmux attach-session -t runway
```

### 14. **Run the Application**
Finally, run the Streamlit application.

```bash
streamlit run app.py
```

---

### Notes:
- Make sure that all necessary ports (e.g., 8501 for Streamlit) are open on your firewall or security group settings to allow external access.
- If you need to stop the app or exit the tmux session, use `CTRL + B` followed by `D` to detach from the tmux session without stopping it.

Let me know if you encounter any issues!
