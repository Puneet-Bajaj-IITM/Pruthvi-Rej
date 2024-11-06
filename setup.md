ssh -i "ml-models-ssh-key.pem" ubuntu@15.207.111.69
git clone https://github.com/Puneet-Bajaj-IITM/Pruthvi-Rej.git
cd Pruthvi-Rej
git checkout -b runway
git pull origin runway

source ./myenv/bin/activate

pip install -r requirements.txt

curl https://ollama.ai/install.sh | sh

nohup ollama serve

sudo apt update
sudo apt install pciutils lshw
ollama pull llama3.1


streamlit run app.py
