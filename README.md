# Bundesliga - OpenLigaDB

Application which I build for pulling the information for the bundlesliga provided by OpenLigaDB.

<a href="https://github.com/python/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/python/black/blob/master/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
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

If you want to simulate the upcoming matches, uncomment the `bundesligainfo.apps.core.openligasdk.openligasdk.py` line: 170.

## Preview

![index_view](https://raw.githubusercontent.com/f0xxx1/bundesliga/master/project_preview/index_upcoming_matchess.png)

![season_view](https://raw.githubusercontent.com/f0xxx1/bundesliga/master/project_preview/season_view.png)

![search_view](https://raw.githubusercontent.com/f0xxx1/bundesliga/master/project_preview/search_view.png)

## License
[MIT](https://choosealicense.com/licenses/mit/)
