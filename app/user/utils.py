import requests
import logging
import jwt
from rest_framework import serializers
from decouple import config


FACEBOOK_APP_ID = config("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = config("FACEBOOK_APP_SECRET")
APPLE_APP_ID = config("APPLE_APP_ID")


def validate_facebook_token(token):
    # The endpoint to debug the token and get its data
    debug_token_url = "https://graph.facebook.com/debug_token"

    # Your Facebook App's Access Token from environment variables (for security)
    app_access_token = FACEBOOK_APP_ID + "|" + FACEBOOK_APP_SECRET

    params = {"input_token": token, "access_token": app_access_token}

    response = requests.get(debug_token_url, params=params)
    data = response.json()

    if response.status_code != 200 and response.status_code != 201:
        logging.error(
            f"Facebook token validation failed with status: {response.status_code}. Response: {data}"
        )
        raise serializers.ValidationError({"token": "Invalid Facebook token."})

    if "error" in data:
        logging.error(f"Facebook token validation error: {data['error']}")
        raise serializers.ValidationError({"token": "Invalid Facebook token."})

    if "data" not in data:
        logging.error("Facebook token validation response missing 'data' key.")
        raise serializers.ValidationError({"token": "Invalid Facebook token."})

    email = data["data"].get("email")
    if not email:
        raise serializers.ValidationError(
            {"email": "Email is missing in Facebook token."}
        )

    return email


# def validate_apple_token(token):
#     """
#     Validate the given Apple token and return the associated email.
#     Note: This is a stubbed version for testing purposes.
#     """

#     # In a real-world scenario, you would send the token to Apple's authentication server.
#     # But for this stubbed version, we'll just return a mock email.

#     # Uncomment and use the below lines when you're ready to implement actual validation:
#     # response = requests.post(APPLE_AUTH_URL, data={'token': token})
#     # data = response.json()
#     # email = data.get('email')
#     # return email

#     return "test.apple@example.com"  # Mocked return for testing purposes


def validate_apple_token(token):
    # Fetch Apple's public keys
    response = requests.get("https://appleid.apple.com/auth/keys")
    keys = response.json()["keys"]

    # Use the keys to decode the token.
    # This verifies the token's signature and ensures it's genuinely from Apple.
    header = jwt.get_unverified_header(token)
    key = [k for k in keys if k["kid"] == header["kid"]][0]
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)

    try:
        # Decode and verify the token
        payload = jwt.decode(
            token, public_key, algorithms=["RS256"], audience=APPLE_APP_ID
        )
    except jwt.InvalidTokenError:
        raise serializers.ValidationError({"token": "Invalid Apple token."})

    email = payload.get("email")
    if not email:
        raise serializers.ValidationError({"email": "Email is missing in Apple token."})

    return email
