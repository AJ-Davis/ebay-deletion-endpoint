from flask import Flask, request, jsonify
import logging
import hashlib
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your verification token for eBay (40 chars, alphanumeric only for maximum compatibility)
VERIFICATION_TOKEN = "0Rq8sTKUCMAwpM0myRAMVlFUaTWQm7f35P8ueVAi"

# Your endpoint URL (without trailing slash)
ENDPOINT_URL = "https://ebay-deletion-endpoint-h5re.onrender.com/ebay/deletion"

@app.route('/ebay/deletion', methods=['GET', 'POST'])
@app.route('/ebay/deletion/', methods=['GET', 'POST'])  # Handle trailing slash
def handle_deletion():
    try:
        logger.info(f"Received {request.method} request to {request.path}")
        logger.info(f"Query params: {request.args}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"User-Agent: {request.headers.get('User-Agent', 'Not provided')}")
        
        if request.method == 'GET':
            # eBay verification challenge
            challenge_code = request.args.get('challenge_code')
            if challenge_code:
                # Use exact approach from eBay's Python documentation
                # m = hashlib.sha256(challengeCode+verificationToken+endpoint);
                hash_string = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
                m = hashlib.sha256(hash_string.encode('utf-8'))
                challenge_response = m.hexdigest()
                
                logger.info(f"Challenge code: {challenge_code}")
                logger.info(f"Verification token: {VERIFICATION_TOKEN}")
                logger.info(f"Endpoint URL: {ENDPOINT_URL}")
                logger.info(f"Hash input: {hash_string}")
                logger.info(f"Challenge response hash: {challenge_response}")
                
                # Return JSON response exactly as eBay expects
                response = {
                    "challengeResponse": challenge_response
                }
                
                return jsonify(response)
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
                
    except Exception as e:
        logger.error(f"Unexpected error in handle_deletion: {e}")
        return f"Error: {str(e)}", 500

@app.route('/test-hash')
def test_hash():
    """Test endpoint to verify hash calculation"""
    try:
        challenge_code = request.args.get('challenge_code', 'test123')
        
        # eBay's exact method
        hash_string = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
        m = hashlib.sha256(hash_string.encode('utf-8'))
        challenge_response = m.hexdigest()
        
        return jsonify({
            "challenge_code": challenge_code,
            "verification_token": VERIFICATION_TOKEN,
            "endpoint_url": ENDPOINT_URL,
            "hash_input": hash_string,
            "challenge_response": challenge_response
        })
    except Exception as e:
        logger.error(f"Error in test_hash: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "endpoint": "ready"}), 200

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        "message": "eBay Deletion Endpoint Service",
        "endpoints": {
            "deletion": "/ebay/deletion",
            "test": "/test-hash",
            "health": "/health"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)