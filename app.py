from flask import Flask, request, jsonify
import csv
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table_of_contents = soup.find("div", id="toc")

    if table_of_contents is None:
        return {"error": "No table of contents found"}

    headings = table_of_contents.find_all("li")
    data = []
    for heading in headings:
        heading_text = heading.find("span", class_="toctext").text
        heading_number = heading.find("span", class_="tocnumber").text
        data.append({
            'heading_number': heading_number,
            'heading_text': heading_text,
        })
    return data

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    data = get_data(url)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
