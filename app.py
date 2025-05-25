from flask import Flask, request, jsonify

app = Flask(__name__)

# Your verification token for eBay
VERIFICATION_TOKEN = "ebay_verification_HAGFN4XqSbHxxto7KPEHDRTJK-uNylGnGbe6QyNiHcM"

@app.route('/ebay/deletion', methods=['GET', 'POST'])
def handle_deletion():
    if request.method == 'GET':
        # eBay verification challenge
        challenge_code = request.args.get('challenge_code')
        if challenge_code:
            # Respond with verification token and challenge code
            response = {
                "challengeResponse": challenge_code,
                "verificationToken": VERIFICATION_TOKEN
            }
            print(f"eBay Verification Challenge: {challenge_code}")
            return jsonify(response)
        else:
            return "eBay Deletion Endpoint - Ready for verification", 200
    
    elif request.method == 'POST':
        # Actual deletion notification
        data = request.json
        print("eBay Deletion Received:", data)
        
        # Process the deletion notification here
        # You can add your business logic to handle user data cleanup
        
        return '', 200

@app.route('/', methods=['GET'])
def health_check():
    return "eBay Deletion Notification Endpoint - Active", 200

if __name__ == '__main__':
    app.run(debug=True)