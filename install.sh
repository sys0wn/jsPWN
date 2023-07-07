mv ../jsPWN ../jsPWNGitCanDelete
mkdir ~/jsPWN
cp requirements.txt ~/jsPWN/
cp jsPWN.py ~/jsPWN/
cd ~/jsPWN
python3 -m venv venv
source ~/jsPWN/venv/bin/activate
pip install -r requirements.txt
echo 'alias jsPWN="python3 ~/jsPWN/jsPWN.py"' > ~/.zshrc
echo 'alias jsPWN="python3 ~/jsPWN/jsPWN.py"' > ~/.bashrc
