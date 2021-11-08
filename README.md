# Scrapping-News-and-Blogs

# This is web scrapping new and blogs of specific cryptocurrency.
In this web-site you can enter any name of cryptocurrency from https://coinmarketcap.com/ and check all related news nad blogs.

### Installation
Copy from source
```bash
git clone https://github.com/Assylken/Scrapping-News-and-Blogs.git
```

### Usage

```
import requests
from requests import Session
import json
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from getId import get_id

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/DBname'
db = SQLAlchemy(app)

session = Session()
```

### Examples

You are typing into input box name of the cryptocurrency. Then get all news and blogs from different websites.
Also if you name isn't correct. Program will display that you entered invalid name.

## License
[MIT](https://choosealicense.com/licenses/mit/)
