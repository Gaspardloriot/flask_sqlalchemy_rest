import jwt
import time
from fastapi import HTTPException, status
from config.app import app
from config.firebase import auth


def get_metabase_token():
    METABASE_SITE_URL = "https://esg-analytics.metabaseapp.com"
    METABASE_SECRET_KEY = "a870839edc82c654354c62c20116f8286afda55f09dc8079728b7fa903e31e00"
    payload = {
        "resource": {"dashboard": 1},
        "params": {},
        "exp": round(time.time()) + (60 * 60)  # 1-hour expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + \
        token + "#theme=night&bordered=true&titled=true"

    return {'iframeUrl': iframeUrl, 'expiry': 60}


def check_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except Exception as e:
        print('------------------- ERROR MESSAGE HERE ---------------------------------')
        print(e)
        print('------------------------------------------------------------------------')
        return False


@app.get("/metabaseconfig/{id_token}")
def get_metabase_config(id_token):
    uid = check_token(id_token)
    if uid != False:
        return get_metabase_token()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token not identified, unauthorized operation',
    )
