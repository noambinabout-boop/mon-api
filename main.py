from fastapi import FastAPI, Request, HTTPException
import os
import hmac
import hashlib
import subprocess
import json


app = FastAPI()


@app.get("/health")
def health():
    return {"Status": "ok"}


@app.post("/webhook")
async def webHooks(request: Request):
    corps = await request.body()

    signature = request.headers.get("X-Hub-Signature-256")
    if signature is None:
        raise HTTPException(status_code=401, detail="Signature absente")

    strip_signature = signature.removeprefix("sha256=")
    cle_webhook = os.environ["WEBHOOK_SECRET"]
    my_key_digested = hmac.new(cle_webhook.encode("utf-8"), corps, hashlib.sha256).hexdigest()

    if hmac.compare_digest(my_key_digested, strip_signature):

        json_request = json.loads(corps.decode("utf-8"))
        if request.headers.get("X-GitHub-Event") != "push":
            return {"Message": "C'est un ping"}
    
        if json_request["ref"] != "refs/heads/main":
            return {"Message": "Pas la bonne branche"}

        subprocess.run("sudo -n /usr/bin/systemctl start --no-block mon-api-deploy.service".split(" "))
        return {"Message": "accepté, traitement en cours"}
    
    raise HTTPException(status_code=401, detail="Les signatures ne sont pas les mêmes")

    


    
