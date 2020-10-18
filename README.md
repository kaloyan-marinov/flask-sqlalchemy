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
sqlite> .schema
...
```

# Resources

1. https://www.youtube.com/watch?v=juPQ04_twtA
2. https://www.youtube.com/watch?v=JI76IvF9Lwg
3. https://www.youtube.com/watch?v=OvhoYbjtiKc
