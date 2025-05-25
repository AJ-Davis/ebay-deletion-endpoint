from flask import Flask, request, jsonify
import logging
import hashlib

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your verification token for eBay (32 chars, alphanumeric only)
VERIFICATION_TOKEN = "SWPIGBT7ZhnEdr6tAoN72FWylgt8dc5O"

# Your endpoint URL (without trailing slash)
ENDPOINT_URL = "https://ebay-deletion-endpoint-h5re.onrender.com/ebay/deletion"

@app.route('/ebay/deletion', methods=['GET', 'POST'])
@app.route('/ebay/deletion/', methods=['GET', 'POST'])  # Handle trailing slash
def handle_deletion():
    logger.info(f"Received {request.method} request to {request.path}")
    logger.info(f"Query params: {request.args}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"User-Agent: {request.headers.get('User-Agent', 'Not provided')}")
    
    if request.method == 'GET':
        # eBay verification challenge
        challenge_code = request.args.get('challenge_code')
        if challenge_code:
            # Create SHA-256 hash: challengeCode + verificationToken + endpoint
            hash_input = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
            logger.info(f"Hash input: {hash_input}")
            
            hash_object = hashlib.sha256(hash_input.encode('utf-8'))
            challenge_response = hash_object.hexdigest()
            
            logger.info(f"Challenge code: {challenge_code}")
            logger.info(f"Verification token: {VERIFICATION_TOKEN}")
            logger.info(f"Endpoint URL: {ENDPOINT_URL}")
            logger.info(f"Challenge response hash: {challenge_response}")
            
            response = {
                "challengeResponse": challenge_response
            }
            
            return jsonify(response), 200, {'Content-Type': 'application/json'}
        else:
            return "eBay Deletion Endpoint - Ready for verification", 200
    
    elif request.method == 'POST':
        # Actual deletion notification
        try:
            data = request.get_json()
            logger.info(f"eBay Deletion Notification Received: {data}")
            
            # Process the deletion notification here
            # You can add your business logic to handle account deletions
            
            return '', 200
        except Exception as e:
            logger.error(f"Error processing deletion notification: {e}")
            return '', 500

@app.route('/test-hash')
def test_hash():
    """Test endpoint to verify hash calculation"""
    challenge_code = request.args.get('challenge_code', 'test123')
    hash_input = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
    hash_object = hashlib.sha256(hash_input.encode('utf-8'))
    challenge_response = hash_object.hexdigest()
    
    return jsonify({
        "challenge_code": challenge_code,
        "verification_token": VERIFICATION_TOKEN,
        "endpoint_url": ENDPOINT_URL,
        "hash_input": hash_input,
        "challenge_response": challenge_response
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "endpoint": "ready"}), 200

if __name__ == '__main__':
    app.run(debug=True)