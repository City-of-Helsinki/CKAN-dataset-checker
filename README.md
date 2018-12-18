# CKAN dataset checker

A set of utilities for checking the outgoing links in a CKAN portal

## Local installation

Clone the repository, then make a virtual environment and install dependencies:
```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
deactivate
```

Specify your metadata urls, email stuff and so on in ```default.conf```.

After that you can just call ```./run.sh```.
