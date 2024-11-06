ssh -i "ml-models-ssh-key.pem" ubuntu@3.111.123.90

git clone https://github.com/Puneet-Bajaj-IITM/Pruthvi-Rej.git

cd Pruthvi-Rej

git checkout -b runway

git pull origin runway

sudo apt update

sudo apt install python3-venv

python3 -m venv myenv

pip install -r requirements.txt

curl https://ollama.ai/install.sh | sh

nohup ollama serve

sudo apt update

sudo apt install pciutils lshw

ollama pull llama3.1

tmux new-session -s mysession  or tmux attach-session -t mysession

source ./myenv/bin/activate

streamlit run app.py
