import requests
import random
from flask import Flask, jsonify, request

app = Flask(__name__)
title = "7AF94"  # Your PlayFab Title ID
secretkey = "GBIPB74594RF9UDYHIAKASEJ1WG66KWWF4FAPKJK1WYZCC94S7"  # Your PlayFab secret key
coems = {}  # Cache for PlayFab IDs

def authjh():
    return {"content-type": "application/json", "X-SecretKey": secretkey}

@app.route("/", methods=["POST", "GET"])
def no():
    return "yesnt"

@app.route('/api/PlayFabAuthentication', methods=['POST'])
def PlayFabAuthentication():
    data = request.get_json()
    print(data)

    CustomId = data.get("CustomId", "Null")
    Nonce = data.get("Nonce", "Null")
    OculusId = data.get("OculusId", "Null")
    Platform = data.get("Platform", "Null")

    # Authenticate with PlayFab
    login_request = requests.post(
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

    if login_request.status_code == 200:
        jsontypeshi = login_request.json()
        goodjson = jsontypeshi.get("data")
        PlayFabId = goodjson.get("PlayFabId")
        SessionTicket = goodjson.get("SessionTicket")
        Entity = goodjson.get("EntityToken")
        EntityToken = Entity["EntityToken"]
        EntityId = Entity["Entity"]["Id"]
        EntityType = Entity["Entity"]["Type"]

        # Link the Custom ID
        linking_response = requests.post(
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

        if linking_response.status_code == 200:
            return jsonify({
                "PlayFabId": PlayFabId,
                "SessionTicket": SessionTicket,
                "EntityToken": EntityToken,
                "EntityId": EntityId,
                "EntityType": EntityType,
                "IsBanned": False
            }), 200
        else:
            return jsonify({"Message": "Failed linking Custom ID"}), 400
    else:
        # Handle the ban error
        errorDetails = login_request.json().get('errorDetails')
        if errorDetails:
            firstBan = next(iter(errorDetails))
            return jsonify({
                "BanMessage": str(firstBan),
                "BanExpirationTime": str(errorDetails[firstBan]),
                "IsBanned": True
            }), 403
        else:
            return jsonify({"Message": "Authentication failed."}), 403

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

@app.route("/cbfn", methods=["POST", "GET"])
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
    if TitleId != '7AF94':
        return jsonify({'Error': 'Bad request', 'Message': 'Invalid titleid!'}), 403
    if Platform != 'Quest':
        return jsonify({'Error': 'Bad request', 'Message': 'Invalid platform!'}), 403

    return jsonify({
        "ResultCode": 1, 
        "StatusCode": 200, 
        "Message": "authed with photon",
        "Result": 0,
        "UserId": UserId,
        "AppId": TitleId,
        "AppVersion": AppVersion,
        "Ticket": Ticket,
        "Token": Token,
        "Nonce": Nonce,
        "Platform": Platform,
        "Username": Username
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
