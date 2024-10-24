from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_chart_data():
    url = "https://www.melon.com/chart/index.htm"
    header_user = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    req = requests.get(url, headers=header_user)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    lst50 = soup.select(".lst50")
    lst100 = soup.select(".lst100")

    lst = lst50 + lst100

    chart_data = []

    for i in lst:
        rank = i.select_one(".rank").text
        song = i.select_one(".ellipsis.rank01").text
        singer = i.select_one(".ellipsis.rank02").text
        album = i.select_one(".ellipsis.rank03").text

        chart_data.append({
            "rank": rank,
            "song": song,
            "singer": singer,
            "album": album
        })
    return chart_data

@app.route('/')
def index():
    chart_data = get_chart_data()
    return render_template('index.html', chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)