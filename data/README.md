
# Bike Sharing Dashboard ✨ 

## Setup Environment - Anaconda  
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
mkdir proyek-analisis-data
cd proyek-analisis-data
pipenv install
pipenv shell
pip install -r requirements.txt

## Run steamlit app
streamlit run dashboard.py


### Notes  
- Adjust the command `streamlit run app.py` according to your file name.  
- Ensure that your `requirements.txt` file is in the same directory as your terminal or command line when you run the pip install command.