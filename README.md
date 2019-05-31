# Bundesliga - OpenLigaDB

Application which I build for pulling the information for the bundlesliga provided by OpenLigaDB.

## Installation

```bash
mkdir bundesliga
virtualenv venv

# depending on OS
# Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\activate

cd bundesliga
git clone https://github.com/f0xxx1/bundesliga.git

pip install -r requirements.txt

# Create a .env file.
# Linux
touch .env

# Windows (PowerShell)
New-Item -Path '.env' -ItemType File

# Copy the content of env.sample into your .env

python manage.py createcachetable
python manage.py runserver

```


## License
[MIT](https://choosealicense.com/licenses/mit/)
