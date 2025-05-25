from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your verification token for eBay (32-80 chars, alphanumeric + underscore + hyphen only)
VERIFICATION_TOKEN = "ebay_verify_5l1Y6H8VbIM0JwjWCl-IoWPVZQgHFvOph_31ddyCrAZ21IwLOw"

@app.route('/ebay/deletion', methods=['GET', 'POST'])
def handle_deletion():
    logger.info(f"Received {request.method} request to /ebay/deletion")
    logger.info(f"Query params: {request.args}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    if request.method == 'GET':
        # eBay verification challenge
        challenge_code = request.args.get('challenge_code')
        if challenge_code:
            # Respond with verification token and challenge code in exact format eBay expects
            response = {
                "challengeResponse": challenge_code,
                "verificationToken": VERIFICATION_TOKEN
            }
            logger.info(f"eBay Verification Challenge: {challenge_code}")
            logger.info(f"Responding with: {response}")
            
            # Return JSON response with proper headers
            resp = jsonify(response)
            resp.headers['Content-Type'] = 'application/json'
            return resp, 200
        else:
            return "eBay Deletion Endpoint - Ready for verification", 200
    
    elif request.method == 'POST':
        # Actual deletion notification
        try:
            data = request.get_json()
            logger.info(f"eBay Deletion Notification Received: {data}")
            print("eBay Deletion Received:", data)
            
            # Process the deletion notification here
            # You can add your business logic to handle user data cleanup
            
            return '', 200
        except Exception as e:
            logger.error(f"Error processing deletion notification: {e}")
            return '', 200

@app.route('/', methods=['GET'])
def health_check():
    return "eBay Deletion Notification Endpoint - Active", 200

@app.route('/health', methods=['GET'])
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)