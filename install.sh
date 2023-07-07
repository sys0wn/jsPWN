mv ../jsPWN ../jsPWNGitCanDelete
cp requirements.txt ~/jsPWN/
cp jsPWN.py ~/jsPWN/
cd ~/jsPWN
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo 'alias jsPWN="python3 ~/jsPWN/jsPWN.py"' > ~/.zshrc
echo 'alias jsPWN="python3 ~/jsPWN/jsPWN.py"' > ~/.bashrc
rm -rf ~/jsPWNGitCanDelete
