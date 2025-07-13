from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import re

app = Flask(__name__)
CORS(app)  

client = MongoClient("mongodb+srv://alodhankhushi17:diyakhushi@cluster0.p4o2q4g.mongodb.net/") #My MongoDB Database
db = client['Grocey_FlexShelf']   #Database Name
products_col = db['FlexShelf_Final']  #Collection Name

@app.route('/search-products', methods=['POST'])
def search_products():
    data = request.get_json()
    query_text = data.get('query', '').strip()

    if not query_text:
        return jsonify([])

    regex = re.compile(f".*{re.escape(query_text)}.*", re.IGNORECASE)

    products = list(products_col.find({
        "$or": [
            {"Product_Name": regex},
            {"Catagory": regex}
        ]
    }, {
        '_id': 0  
    }))

    print(f"🔍 Query received: {query_text}")
    print(f"✅ Matched {len(products)} products")

    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)