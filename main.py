import requests
import env
from datetime import datetime, timezone
import json
import hmac
import hashlib
import sys

def compute_signed_sha256(plaintxt: str):
    return hmac.new(
        key=bytes(env.SIGNING_SECRET, 'utf-8'),
        msg=plaintxt.encode("utf-8"), 
        digestmod=hashlib.sha256
    ).hexdigest()

def prepare_submission():
    body = {
        "timestamp":  datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "name": env.NAME,
        "email": env.EMAIL,
        "resume_link": env.RESUME_LINK,
        "repository_link": env.REPOSITORY_LINK,
        "action_run_link": env.ACTION_RUN_LINK
    }

    body_as_json_str = json.dumps(body, ensure_ascii=False)

    signed_sha256 = compute_signed_sha256(body_as_json_str)

    headers = {
        'Content-Type': 'application/json',
        'X-Signature-256': f"sha256={signed_sha256}"
    }

    return {
        "url": env.API_URL,
        "body": body_as_json_str,
        "headers": headers
    }
    


def post_submission():
    submission = prepare_submission()

    response = requests.post(
        url=submission["url"],
        data=submission["body"],
        headers=submission["headers"]
    )
    
    if response.status_code != 200:
        print('failure!')
        print(response.status_code)
        print(response.text)
        sys.exit(1)
        return
    
    response_body = response.json()

    print(f"submission receipt = {response_body.receipt}")
    

def main():
    post_submission()


if __name__ == "__main__":
    main()
