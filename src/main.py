import requests
from requests import Session
import json
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from getId import get_id

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aizhan1212@localhost/PythonAssignment'
db = SQLAlchemy(app)

session = Session()


class Store(db.Model):
    __tablename__ = 'store'
    id = db.Column('id', db.Integer, primary_key = True)
    all_text = db.Column('all_text', db.Unicode)
    def __init__(self, id, all_text):
        self.id = id
        self.all_text = all_text


@app.route('/coin', methods=['GET', 'POST'])
def coin():
	if request.method == 'POST':
		bitcoin_name = request.form['cryptocurrency']
		res = parsing(bitcoin_name)
		if res == 'Error':
			return jsonify(status = 'Invalid cryptocurrency name!')
		ARTICLE = ' '.join(res)
		ARTICLE = ARTICLE.replace('.', '.<eos>')
		ARTICLE = ARTICLE.replace('?', '?<eos>')
		ARTICLE = ARTICLE.replace('!', '!<eos>')
		max_chunk = 250
		sentences = ARTICLE.split('<eos>')
		current_chunk = 0 
		chunks = []
		for sentence in sentences:
    			if len(chunks) == current_chunk + 1: 
        			if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
            				chunks[current_chunk].extend(sentence.split(' '))
        			else:
            				current_chunk += 1
            				chunks.append(sentence.split(' '))
    			else:
        			print(current_chunk)
       				chunks.append(sentence.split(' '))
		for chunk_id in range(len(chunks)):
    			chunks[chunk_id] = ' '.join(chunks[chunk_id])
		total_str = ""
		for i in chunks:
			total_str += '<p>' + str(i) + '</p>'


		bitcoin_id = get_id(bitcoin_name.lower())
		info = Store(bitcoin_id, total_str)
		db.session.add(info)
		db.session.commit()

		str_answer = Store.query.filter_by(id = bitcoin_id).first()
		db.session.commit()
		print(str_answer.all_text)
		
		return '''

			<p>{}</p>
		
		'''.format(str_answer.all_text) 

	else:
		return '''
		<form method="POST">
               <input style = "border: 2px solid black; height: 45px; width: 250px; font-size: 15px; " type="text" name="cryptocurrency">
               <input style = "border: 2px solid black; height: 45px; width: 90px;" type="submit" value="Check">
		</form>
		'''

def getUrls(name):
	get_url_news = 'https://api.coinmarketcap.com/content/v3/news?coins=%s'
	coin_id = get_id(name.lower())
	url = get_url_news %coin_id
	response = session.get(url)
	data = json.loads(response.text)
	if data['status']['error_code'] == '500':
		return 'Error'
	leng = (len(data['data']))
	thislist = []
	for i in range(leng):
		thislist.append(data['data'][i]['meta']['sourceUrl'])
	return thislist

def parsing(name):
	lst = getUrls(name)
	if lst == 'Error':
		return 'Error'
	ans = []
	for i in lst:
		cookies = dict(BCPermissionLevel='PERSONAL')
		req = requests.get(i, headers={"User-Agent": "Mozilla/5.0"}, cookies=cookies)
		soup = BeautifulSoup(req.content, 'html.parser')
		tmp = soup.find_all('p')
		for i in tmp:
			ans.append(i.get_text())
	return ans

if __name__ == '__main__':
     app.run(debug=True)
