Setup Environment - Shell/Terminal

mkdir submission
cd submission

Setup Environment - Virtual Environment (venv)

python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # Mac/Linux
pip install -r requirements.txt

Setup Environment - Pipenv

pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt

Run Streamlit App
Jalankan perintah berikut dari folder submission:
streamlit run dashboard/dashboard.py