# Versioned Pastebin

### Packages Used:
- Flask
- SQLAlchemy
- Flask-RESTful
- Marshmallow
- pseudobabble/repository


### Usage

```
git clone [this-repo]
cd [this-repo]
virtualenv --python=/usr/bin/python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
curl 127.0.0.1:5000/documents/first-title -d '{"content": "foo"}'  -H 'Content-Type: application/json'
curl 127.0.0.1:5000/documents/first-title
curl 127.0.0.1:5000/documents/first-title/2020-01-01-01:01:01
curl 127.0.0.1:5000/documents/first-title/latest
```
