from flask import Flask, request

app = Flask(__name__)

@app.route('/ebay/deletion', methods=['POST'])
def handle_deletion():
    data = request.json
    print("eBay Deletion Received:", data)
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)