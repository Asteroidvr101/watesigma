import requests
import random
from flask import Flask, jsonify, request

app = Flask(__name__)
title = "7AF94"
secretkey = "GBIPB74594RF9UDYHIAKASEJ1WG66KWWF4FAPKJK1WYZCC94S7"  
ApiKey = "OC|9837791239572874|4523778edb61de7362b2843a78428242"
coems = {}

def authjh():
    return {"content-type": "application/json", "X-SecretKey": secretkey}

@app.route("/", methods=["POST", "GET"])
def no():
    return "yesnt"

@app.route('/api/PlayFabAuthentication', methods=["POST", "GET"])
def PlayFabAuthentication():
    CustomId: str = data.get("CustomId", "Null")
    Nonce: str = data.get("Nonce", "Null")
    OculusId: str = data.get("OculusId", "Null")
    Platform: str = data.get("Platform", "Null")
    AppId: str = data.get("AppId", "Null")

    if 'UnityPlayer' not in request.headers.get('User-Agent', ' '):
        return jsonify({
            "BanMessage": "Your account has been traced and you have been banned.",
            "BanExpirationTime": "Indefinite"
        }), 403
    
    data = request.get_json()    
    print(data)
    BLAH = requests.post(
        url=f"https://{title}.playfabapi.com/Server/LoginWithServerCustomId",
        json={
            "ServerCustomId": CustomId,
            "CreateAccount": True
        },
        headers={
            "content-type": "application/json",
            "x-secretkey": secretkey
        }
    )
    
    if BLAH.status_code == 200: 
        print("successful login chat!")
        jsontypeshi = BLAH.json()
        goodjson = jsontypeshi.get("data")
        PlayFabId = goodjson.get("PlayFabId")
        SessionTicket = goodjson.get("SessionTicket")
        Entity = goodjson.get("EntityToken")
        EntityToken = Entity["EntityToken"]
        EntityId = Entity["Entity"]["Id"]
        EntityType = Entity["Entity"]["Type"]

        data = [
            PlayFabId,
            SessionTicket,
            Entity,
            EntityToken,
            EntityId,
            Nonce,
            OculusId,
            Platform
        ]

        EASports = requests.post(
            url=f"https://{title}.playfabapi.com/Client/LinkCustomID",
            json={
                "CustomID": CustomId,
                "ForceLink": True
            },
            headers={
                "content-type": "application/json",
                "x-authorization": SessionTicket
            }
        )
        if EASports.status_code == 200:
            print("Ok, linked it ig")
            return jsonify({
                "PlayFabId": PlayFabId,
                "SessionTicket": SessionTicket,
                "EntityToken": EntityToken,
                "EntityId": EntityId,
                "EntityType": EntityType
            }), 200
        else:
            return jsonify({"Message": "Failed to link"}), 400

    elif BLAH.status_code == 403:
        ban_info = BLAH.json()
        if ban_info.get('errorCode') == 1002:
            ban_message = ban_info.get('errorMessage', "No ban message provided.")
            ban_details = ban_info.get('errorDetails', {})
            ban_expiration_key = next(iter(ban_details.keys()), None)
            ban_expiration_list = ban_details.get(ban_expiration_key, [])
            ban_expiration = ban_expiration_list[0] if len(ban_expiration_list) > 0 else "No expiration date provided."
            print(ban_info)
            return jsonify({
                'BanMessage': ban_expiration_key,
                'BanExpirationTime': ban_expiration
            }), 403
        else:
            error_message = ban_info.get('errorMessage', 'Forbidden without ban information.')
            return jsonify({
                'Error': 'PlayFab Error',
                'Message': error_message
            }), 403
    else:
        error_info = BLAH.json()
        error_message = error_info.get('errorMessage', 'An error occurred.')
        return jsonify({
            'Error': 'PlayFab Error',
            'Message': error_message
        }), BLAH.status_code

@app.route("/api/CachePlayFabId", methods=["POST"])
def cpi():
    getjson = request.get_json()
    coems[getjson.get("PlayFabId")] = getjson
    return jsonify({"Message": "worked1!!"}), 200

@app.route("/api/titledata", methods=["POST", "GET"])
def real():
    realshit = f"https://{title}.playfabapi.com/Server/GetTitleData"
    blah = {"X-SecretKey": secretkey, "Content-Type": "application/json"}
    e = requests.post(url=realshit, headers=blah)
    sigmarizzauth = e.json().get("data", "").get("Data", "")
    return jsonify(sigmarizzauth)

@app.route("/api/ConsumeOculusIAP", methods=["POST"])
def consume_oculus_iap():
    rjson = request.get_json()

    access_token = rjson.get("userToken")
    user_id = rjson.get("userID")
    nonce = rjson.get("nonce")
    sku = rjson.get("sku")

    response = requests.post(
        url=f"https://graph.oculus.com/consume_entitlement?nonce={nonce}&user_id={user_id}&sku={sku}&access_token={settings.ApiKey}",
        headers={"content-type": "application/json"}
    )

    if response.json().get("success"):
        return jsonify({"result": True})
    else:
        return jsonify({"error": True})

@app.route("/cbfn", methods=["POST","GET"])
def cfbn():
    name = request.args.get('name')
    BadNames = [
        "KKK", "PENIS", "NIGG", "NEG", "NIGA", "MONKEYSLAVE", "SLAVE", "FAG", 
        "NAGGI", "TRANNY", "QUEER", "KYS", "DICK", "PUSSY", "VAGINA", "BIGBLACKCOCK", 
        "DILDO", "HITLER", "KKX", "XKK", "NIGA", "NIGE", "NIG", "NI6", "PORN", 
        "JEW", "JAXX", "TTTPIG", "SEX", "COCK", "CUM", "FUCK", "PENIS", "DICK", 
        "ELLIOT", "JMAN", "K9", "NIGGA", "TTTPIG", "NICKER", "NICKA", 
        "REEL", "NII", "@here", "!", " ", "JMAN", "PPPTIG", "CLEANINGBOT", "JANITOR", "K9", 
        "H4PKY", "MOSA", "NIGGER", "NIGGA", "IHATENIGGERS", "@everyone", "TTT"
    ]
    result = 0 if name not in BadNames else 2
    return jsonify({"Message": "the name thingy worked!", "Name": name, "Result": result})

@app.route("/gaa", methods=["POST", "GET"])
def gaa():
    getjson = request.get_json()["FunctionResult"]
    return jsonify(getjson)

@app.route("/saa", methods=["POST", "GET"])
def saa():
    getjson = request.get_json()["FunctionResult"]
    return jsonify(getjson)

@app.route("/grn", methods=["POST", "GET"])
def grn():
    return jsonify({"result": f"pluh!{random.randint(1000, 9999)}"})

@app.route("/api/photon", methods=["POST"])
def photonauth():
    getjson = request.get_json()
    Ticket = getjson.get("Ticket")
    Nonce = getjson.get("Nonce")
    TitleId = getjson.get("AppId")
    Platform = getjson.get("Platform")
    UserId = getjson.get("UserId")
    AppVersion = getjson.get("AppVersion")
    Token = getjson.get("Token")
    Username = getjson.get("username")
    if Nonce is None:
        return jsonify({'Error': 'Bad request', 'Message': 'Not Authenticated!'}), 304 
    if TitleId != '910A2':
        return jsonify({'Error': 'Bad request', 'Message': 'Invalid titleid!'}), 403
    if Platform != 'Quest':
        return jsonify({'Error': 'Bad request', 'Message': 'Invalid platform!'}), 403
    return jsonify({"ResultCode": 1, "StatusCode": 200, "Message": "authed with photon",
                    "Result": 0,
                    "UserId": UserId,
                    "AppId": TitleId,
                    "AppVersion": AppVersion,
                    "Ticket": Ticket,
                    "Token": Token,
                    "Nonce": Nonce,
                    "Platform": Platform,
                    "Username": Username}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
