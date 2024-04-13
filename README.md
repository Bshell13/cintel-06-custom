# MLB Stats for Module 06
Updated stats for KC Royals.

## Virtual Environment
Create a virtual environment and activate after successful creation.
```shell
py -m venv .venv
.venv\Sctipts\activate
```

## Installing External Libraries
list of external libraries
-  pandas
-  shiny
-  shiny live
-  python-mlb-statsapi
-  shinyswatch
-  shinywidgets
-  faicons
```shell
py -m pip install "list of external libraries"
py -m pip freeze > requirements.txt
```

## Running PyShiny Locally
Running the app locally for quick updates.
```shell
shiny run --reload --launch-browser dashboard/app.py
```

## After Making Changes, Export to GitHub Docs Folder
Export to docs folder and test GitHub Pages locally.
```shell
shiny static-assets remove
shinylive export dashboard docs
py -m http.server --directory docs --bind localhost 8008
```