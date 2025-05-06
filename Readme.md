install packages

```
pip install -r requirements.txt
```

start program

```
python init.py
```

debugger

```
uvicorn app.main:app --host localhost --port 8000 --reload
```

export requirements

```
pip freeze > requirements.txt
```

test

```
pytest
```

package

```
pyinstaller --onefile init.py --name i3s_server
```
