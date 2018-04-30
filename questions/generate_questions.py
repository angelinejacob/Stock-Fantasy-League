"""Generate quiz questions daily."""
import psycopg2
import psycopg2.extras
import os
from urllib.parse import urlparse
import string
import random
from requests import get


# init postgresql connection
def generate(cur):
    """Generate quiz questions."""
    # Question 1
    q1 = "Which of these stock symbols is not real?"
    e1 = "One of these stock symbols is not listed on the three major stock exchanges. Stock symbols are unique identifiers for companies on an exchange. "
    cur.execute('SELECT symbol, name FROM stockdata ORDER BY RANDOM() LIMIT 2')
    x = cur.fetchone()
    a11 = x['symbol']
    e11 = "This symbol is for " + x['name']
    x = cur.fetchone()
    a12 = x['symbol']
    e12 = "This symbol is for " + x['name']
    while True:
        a13 = ''.join(random.choices(string.ascii_uppercase, k=random.randint(1, 4)))
        cur.execute("SELECT COUNT(*) FROM stockdata WHERE symbol LIKE '%s'" % a13)
        if cur.fetchone()['count'] == 0:
            break
    e13 = "This symbol does not exist."
    print(q1)
    print(a11)
    print(a12)
    print(a13)
    print()

    q2 = "Which of these stocks has the highest price?"
    e2 = "A stock's price represents its value to investors. Stocks with a higher price represent a higher value to investors. "
    cur.execute('SELECT symbol, price FROM stockdata ORDER BY RANDOM() LIMIT 3')
    u = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey=DEDSQFY460FDRASD&symbol="
    ans = []
    for s in cur.fetchall():
        s = s['symbol']
        data = get(u + s).json()
        data = data['Time Series (Daily)']
        data = data[list(data.keys())[0]]
        ans.append((s, float(data['4. close'])))
    ans = sorted(ans, key=lambda k: k[1])
    a21 = ans[0][0]
    e21 = "This stock's price is " + str(ans[0][1])
    a22 = ans[1][0]
    e22 = "This stock's price is " + str(ans[1][1])
    a23 = ans[2][0]
    e23 = "This stock's price is " + str(ans[2][1])
    print(q2)
    print(a21)
    print(a22)
    print(a23)
    print()

    q3 = "Which of these stocks has the highest volume?"
    e3 = "Volume is the number of times a company's stocks are traded each day. More popular stocks generally have a higher volume."
    cur.execute('SELECT symbol FROM stockdata ORDER BY RANDOM() LIMIT 3')
    u = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey=DEDSQFY460FDRASD&symbol="
    ans = []
    for s in cur.fetchall():
        s = s['symbol']
        data = get(u + s).json()
        data = data['Time Series (Daily)']
        data = data[list(data.keys())[0]]
        ans.append((s, int(data['5. volume'])))
    ans = sorted(ans, key=lambda k: k[1])
    a31 = ans[0][0]
    e31 = "This stock's volume is " + str(ans[0][1])
    a32 = ans[1][0]
    e32 = "This stock's volume is " + str(ans[1][1])
    a33 = ans[2][0]
    e33 = "This stock's volume is " + str(ans[2][1])
    print(q3)
    print(a31)
    print(a32)
    print(a33)
    print()

    q4 = "Which of these stocks is doing historically well?"
    e4 = "Historical performance can be gauged by comparing a stock's price to its 52 week high and low. A stock near its 52 week high is performing well. "
    cur.execute('SELECT symbol FROM stockdata ORDER BY RANDOM() LIMIT 3')
    u = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey=DEDSQFY460FDRASD&outputsize=full&symbol="
    ans = []
    for s in cur.fetchall():
        s = s['symbol']
        data = get(u + s).json()
        data = data['Time Series (Daily)']
        price = float(data[list(data.keys())[0]]['4. close'])
        keys = list(data.keys())[:253]
        data = [data[k] for k in keys]
        pmax = 0
        pmin = 1e100
        for d in data:
            pmax = max(pmax, float(d['2. high']))
            pmin = min(pmin, float(d['3. low']))
        rp = (price - pmin) / pmin
        ans.append((s, rp, pmin, pmax, price))
    ans = sorted(ans, key=lambda k: k[1])
    a41 = ans[0][0]
    e41 = "This stock's 52 week low is " + str(ans[0][2]) + " and its 52 week high is " + str(ans[0][3]) + ". It's current price is " + str(ans[0][4])
    a42 = ans[1][0]
    e42 = "This stock's 52 week low is " + str(ans[1][2]) + " and its 52 week high is " + str(ans[1][3]) + ". It's current price is " + str(ans[1][4])
    a43 = ans[2][0]
    e43 = "This stock's 52 week low is " + str(ans[2][2]) + " and its 52 week high is " + str(ans[2][3]) + ". It's current price is " + str(ans[2][4])
    print(q4)
    print(a41)
    print(a42)
    print(a43)
    print()

    q5 = "Which of these stocks belongs in the sector: "
    e5 = "Stock's can be separated into sectors. All stocks in a sector are related in some way, thus their share prices are related."
    sector = random.choice(("Utilities", "Health Care", "Financials", "Industrials", "Materials"))
    q5 += sector + "?"
    cur.execute("SELECT symbol FROM stockdata WHERE sector LIKE '%s' ORDER BY RANDOM() LIMIT 2" % sector)
    a51 = cur.fetchone()['symbol']
    e51 = "This stock is in the sector: " + sector
    a52 = cur.fetchone()['symbol']
    e52 = "This stock is in the sector: " + sector
    cur.execute("SELECT symbol, sector FROM stockdata WHERE sector NOT LIKE '%s' ORDER BY RANDOM() LIMIT 1" % sector)
    x = cur.fetchone()
    a53 = x['symbol']
    e53 = "This stock is in the sector: " + x['sector']
    print(q5)
    print(a51)
    print(a52)
    print(a53)
    print()

    q6 = "Which of these stocks is most volatile?"
    e6 = "One measure of a stock's volatility is its 52 week range. A larger range predicts higher volatility."
    cur.execute('SELECT symbol FROM stockdata ORDER BY RANDOM() LIMIT 3')
    u = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey=DEDSQFY460FDRASD&outputsize=full&symbol="
    ans = []
    for s in cur.fetchall():
        s = s['symbol']
        data = get(u + s).json()
        data = data['Time Series (Daily)']
        price = float(data[list(data.keys())[0]]['4. close'])
        keys = list(data.keys())[:253]
        data = [data[k] for k in keys]
        pmax = 0
        pmin = 1e100
        for d in data:
            pmax = max(pmax, float(d['2. high']))
            pmin = min(pmin, float(d['3. low']))
        prange = (pmax - pmin) / ((pmax + pmin) / 2)
        ans.append((s, prange, pmax, pmin))
    ans = sorted(ans, key=lambda k: k[1])
    a61 = ans[0][0]
    e61 = "This stock's 52 week low is " + str(ans[0][2]) + " and its 52 week high is " + str(ans[0][3])
    a62 = ans[1][0]
    e62 = "This stock's 52 week low is " + str(ans[1][2]) + " and its 52 week high is " + str(ans[1][3])
    a63 = ans[2][0]
    e63 = "This stock's 52 week low is " + str(ans[2][2]) + " and its 52 week high is " + str(ans[2][3])
    print(q6)
    print(a61)
    print(a62)
    print(a63)
    print()

    q7 = "Which sector is doing best?"
    e7 = "Stocks in a sector are affected by world events in a similar manner. Their prices therefore move similarly."
    u = "https://www.alphavantage.co/query?function=SECTOR&apikey=DEDSQFY460FDRASD&outputsize=full"
    res = get(u).json()['Rank B: 1 Day Performance']
    sectors = random.sample(("Utilities", "Health Care", "Financials", "Industrials", "Materials"), 3)
    data = []
    for s in sectors:
        data.append((s, float(res[s][:-1])))
    data = sorted(data, key=lambda k: k[1])

    a71 = data[0][0]
    e71 = "The performance of %s is %f%%" % data[0]
    a72 = data[1][0]
    e72 = "The performance of %s is %f%%" % data[1]
    a73 = data[2][0]
    e73 = "The performance of %s is %f%%" % data[2]
    print(q7)
    print(a71)
    print(a72)
    print(a73)
    print()

    cur.execute('TRUNCATE TABLE question RESTART IDENTITY;')
    cur.execute("INSERT INTO question (question, answers, answer_index, answer_descriptions, overall_description) VALUES (%s, %s, %s, %s, %s)", (q1, [a11, a12, a13], 2, [e11, e12, e13], e1))
    cur.execute("INSERT INTO question (question, answers, answer_index, answer_descriptions, overall_description) VALUES (%s, %s, %s, %s, %s)", (q2, [a21, a22, a23], 2, [e21, e22, e23], e2))
    cur.execute("INSERT INTO question (question, answers, answer_index, answer_descriptions, overall_description) VALUES (%s, %s, %s, %s, %s)", (q3, [a31, a32, a33], 2, [e31, e32, e33], e3))
    cur.execute("INSERT INTO question (question, answers, answer_index, answer_descriptions, overall_description) VALUES (%s, %s, %s, %s, %s)", (q4, [a41, a42, a43], 2, [e41, e42, e43], e4))
    cur.execute("INSERT INTO question (question, answers, answer_index, answer_descriptions, overall_description) VALUES (%s, %s, %s, %s, %s)", (q5, [a51, a52, a53], 2, [e51, e52, e53], e5))
    cur.execute("INSERT INTO question (question, answers, answer_index, answer_descriptions, overall_description) VALUES (%s, %s, %s, %s, %s)", (q6, [a61, a62, a63], 2, [e61, e62, e63], e6))
    cur.execute("INSERT INTO question (question, answers, answer_index, answer_descriptions, overall_description) VALUES (%s, %s, %s, %s, %s)", (q7, [a71, a72, a73], 2, [e71, e72, e73], e7))
    return {"q1": {"text": q1, "answers": [a11, a12, a13], "explanations": [e11, e12, e13], "explanation": e1},
            "q2": {"text": q2, "answers": [a21, a22, a23], "explanations": [e21, e22, e23], "explanation": e2},
            "q3": {"text": q3, "answers": [a31, a32, a33], "explanations": [e31, e32, e33], "explanation": e3},
            "q4": {"text": q4, "answers": [a41, a42, a43], "explanations": [e41, e42, e43], "explanation": e4},
            "q5": {"text": q5, "answers": [a51, a52, a53], "explanations": [e51, e52, e53], "explanation": e5},
            "q6": {"text": q6, "answers": [a61, a62, a63], "explanations": [e61, e62, e63], "explanation": e6},
            "q7": {"text": q7, "answers": [a71, a72, a73], "explanations": [e71, e72, e73], "explanation": e7}}

if __name__ == "__main__":
    try:
        url = urlparse(os.environ["DATABASE_URL"])
    except:
        url = urlparse("postgres://xqeuyuquhktxoq:c7869c5a14cb7f47eea6a586dbc23ffe5ee8522abfb2c3c4b2b0785db64b5916@ec2-54-243-239-66.compute-1.amazonaws.com:5432/den0hekga678pn")
    db_conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    cur = db_conn.cursor()
    generate(cur)
    db_conn.commit()
