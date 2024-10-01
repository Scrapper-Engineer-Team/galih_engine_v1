## Requirement
- Virual Environtment
- Pyhton 3.10 up
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## How to Run
```
$ python3 main.py -n [Class_Name] -u [url] -d [Destination_S3_Or_Local]
```

## Struktur Data
- Controller is directory for engine crawling
- Lib is a directory for all libraries like data store, produce kafka and other libraries