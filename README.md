# Instructions

```
$ python3 --version
Python 3.8.3

$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
(venv) $ pre-commit install
```

Running each of the scripts creats its own `*.db` file.
To run each script and to explore its created file, you can start with the following
commands:
```
(venv) $ python ex_1_one_to_many.py
(venv) $ sqlite3 ex_1_one_to_many.db
sqlite> .mode columns
sqlite> .headers on
sqlite> .tables
sqlite> .schema
...
```

# Initial resources

1. "Creating One-To-Many Relationships in Flask-SQLAlchemy" is a [video tutorial available on YouTube](https://www.youtube.com/watch?v=juPQ04_twtA)

2. "One to One Relationships in Flask-SQLAlchemy" is a [video tutorial available on YouTube](https://www.youtube.com/watch?v=JI76IvF9Lwg)

3. "Creating Many-To-Many Relationships in Flask-SQLAlchemy" is a [video tutorial available on YouTube](https://www.youtube.com/watch?v=OvhoYbjtiKc]

# `2021/03/19/07_54/g-t-i-17/specify-an-ondelete-cascade-option-in-the-Person-db-model`

There is a thread on Reddit that appears to build upon the video tutorials mentioned in the previous section. That thread is on https://www.reddit.com/r/flask/comments/fjwua7/flasksqlalchemy_ondeletecascade_not_working_in/
