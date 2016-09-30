# Plankton - html to pdf REST service

Uses wkhtmltopdf as backend.
Only works with python 3.5 or greater.

Enspired by:
https://github.com/openlabs/docker-wkhtmltopdf and https://github.com/incuna/django-wkhtmltopdf.

## Installation
1. ```pip install plankton``` 
2. download and install wkhtmltopdf http://wkhtmltopdf.org/downloads.html.
3. Run server```plankton-server``` 

If you want to run in docker container:
1. Clone repo ```git clone git@github.com:django-stars/plankton.git```
2. ```cd plankton```
3. Build docker image ```docker build -t plankton .```
4. Run container  ```docker run -p 9003:8080  plankton```.

You can specify wkhtmltopdf command and port:
```plankton-server --wkhtmltopdf_command '/usr/local/bin/wkhtmltopdf' --port 9000```


## Usage

POST ```http://127.0.0.1:9003/html-to-pdf/```

DATA ```{"page": "http://google.com.ua"}```

You can provide wkhtmltopdf options:

DATA ```{"page": "http://google.com.ua", "options": {"javascript-delay": 2000, "cookie": [["key1","val1"], ["key2", "val2"]]}}```


## TODO
Project currently under developing and there are lot of things to do:

1. debug mode
2. HTTP OPTIONS
3. logging
4. security
5. ...



