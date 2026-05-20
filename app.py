from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json, os
app = Flask(__name__)
ORDERS_FILE = "orders.txt"
MENU = {"Kiss me, Katsu":85,"Pretty in Shanghai":70,"Crispy Queen":90,"Soft girl Flakes":80,"Bacon me Blush":85,"Siomai Babe":65}
DELIVERY_FEE=20

def get_next_num():
    if not os.path.exists(ORDERS_FILE): return 1
    with open(ORDERS_FILE) as f: lines=[l.strip()for l in f if l.strip()]
    return 1 if not lines else json.loads(lines[-1])["order_num"]+1

@app.route('/')
def index(): return render_template('index.html',menu=MENU)

@app.route('/place-order',methods=['POST'])
def place_order():
    d=request.get_json()
    subt=sum(MENU[i]*int(q)for i,q in d['order'].items())
    df=DELIVERY_FEE if d['order_type']=='delivery'else 0
    rec={"order_num":get_next_num(),"dt":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"cust_name":d['cust_name'],"type":d['order_type'],"loc":d['location'],"items":[{"n":i,"q":q,"p":MENU[i],"s":MENU[i]*q}for i,q in d['order'].items()],"sub":subt,"df":df,"tot":subt+df}
    with open(ORDERS_FILE,'a')as f:f.write(json.dumps(rec)+"\n")
    return jsonify({"success":True,"receipt":rec})

@app.route('/get-orders')
def get_orders():
    orders,ts,td=[],0,0
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE)as f:
            for l in f:
                if l.strip():o=json.loads(l);orders.append(o);ts+=o['tot'];td+=o['df']
    return jsonify({"orders":orders,"total_sales":ts,"total_delivery":td})

if __name__=='__main__':app.run(debug=True)