import requests
import random
from flask import Flask, jsonify, request

app = Flask(__name__)
title = "7AF94"
secretkey = "GBIPB74594RF9UDYHIAKASEJ1WG66KWWF4FAPKJK1WYZCC94S7"
ApiKey = "OC|9837791239572874|4523778edb61de7362b2843a78428242"

coems = {}
banned_users = {}

def authjh():
    return {"content-type": "application/json", "X-SecretKey": secretkey}

@app.route("/", methods=["POST", "GET"])
def no():
    return "yesnt"

@app.route('/api/PlayFabAuthentication', methods=["POST", "GET"])
def PlayFabAuthentication():
    if 'UnityPlayer' not in request.headers.get('User-Agent', ''):
        return jsonify({
            "BanMessage": "Your account has been traced and you have been banned.",
            "BanExpirationTime": "Indefinite"
        }), 403
        
    data = request.get_json()
    rjson = request.get_json()
    oculus_id = rjson.get('OculusId')
    nonce = rjson.get("Nonce")

    oculus_response = requests.post("https://graph.oculus.com/user_nonce_validate", json={
        "access_token": f"",
        "nonce": nonce,
        "user_id": oculus_id
    })
    print(oculus_response.status_code)
    print(oculus_response)
    if oculus_response.status_code != 200 or not oculus_response.json().get("is_valid", False):
        return jsonify({
            "BanMessage": "Your account has been traced and you have been banned.",
            "BanExpirationTime": "Indefinite"
        }), 403
    if not data:
        return jsonify({"Message": "Missing JSON body"}), 400

    CustomId: str = data.get("CustomId", "Null")
    Nonce: str = data.get("Nonce", "Null")
    OculusId: str = data.get("OculusId", "Null")
    Platform: str = data.get("Platform", "Null")
    AppId: str = data.get("AppId", "Null")

    if CustomId is None:
        return jsonify({"Message": "Missing CustomId parameter", "Error": "BadRequest-NoCustomId"}), 400
    if Nonce is None:
        return jsonify({"Message": "Missing Nonce parameter", "Error": "BadRequest-NoNonce"}), 400
    if AppId is None:
        return jsonify({"Message": "Missing AppId parameter", "Error": "BadRequest-NoAppId"}), 400
    if Platform is None:
        return jsonify({"Message": "Missing Platform parameter", "Error": "BadRequest-NoPlatform"}), 400
    if OculusId is None:
        return jsonify({"Message": "Missing OculusId parameter", "Error": "BadRequest-NoOculusId"}), 400
    if AppId != title:
        return jsonify({"Message": "Request sent for the wrong App ID", "Error": "BadRequest-AppIdMismatch"}), 400
    if not CustomId.startswith("OC") and not CustomId.startswith("PI"):
        return jsonify({"Message": "Bad request", "Error": "BadRequest-No OC or PI Prefix"}), 400

    missing_fields = not CustomId or not Nonce or not OculusId or not Platform or not AppId
    if missing_fields:
        return jsonify({"Message": "error!", "Error": "no"}), 400

    if AppId != title:
        return jsonify({"Message": "skkod", "Error": "skid??"}), 400

    if not CustomId.startswith("OCULUS"):
        return jsonify({"Message": "scary hacker!!", "Error": "ahcker"}), 400

    if not Platform.startswith("Quest"):
        return jsonify({"Message": "scary hacker!!", "Error": "ahcker"}), 400

    if Platform == "Steam" and (CustomId.startswith("OC") or CustomId.startswith("PI")):
        return jsonify({
            "Message": "UNABLE TO AUTHENTICATE YOUR OCULUS ACCOUNT! TRY RESTARTING THE GAME, YOUR HEADSET, ADD GORILLA TAG AGAIN FROM THE STORE, OR REINSTALLING IF THIS ERROR PERSISTS"
        }), 403

    if CustomId in banned_users:
        return jsonify({
            "Message": f"User is banned for using disallowed platform or unauthorized modifications ('{banned_users[CustomId]}')."
        }), 403

    disallowed_platforms = ["PCVR", "Steam", "DLL"]
    if Platform in disallowed_platforms or "dll" in CustomId.lower():
        banned_users[CustomId] = Platform if Platform in disallowed_platforms else "DLL"
        return jsonify({
            "Message": f"User banned for attempting to use disallowed platform or unauthorized DLL ('{Platform or 'DLL'}')."
        }), 403

    # Request to PlayFab Login
    login_request = requests.post(
        url=f"https://{title}.playfabapi.com/Server/LoginWithServerCustomId",
        json={"ServerCustomId": CustomId, "CreateAccount": True},
        headers=authjh()
    )

    if login_request.status_code == 200:
        data = login_request.json().get("data")
        session_ticket = data.get("SessionTicket")
        entity_token = data.get("EntityToken").get("EntityToken")
        playfab_id = data.get("PlayFabId")
        entity_type = data.get("EntityToken").get("Entity").get("Type")
        entity_id = data.get("EntityToken").get("Entity").get("Id")

        link_response = requests.post(
            url=f"https://{title}.playfabapi.com/Server/LinkServerCustomId",
            json={
                "ForceLink": True,
                "PlayFabId": playfab_id,
                "ServerCustomId": CustomId,
            },
            headers=authjh()
        ).json()

        return jsonify({
            "PlayFabId": playfab_id,
            "SessionTicket": session_ticket,
            "EntityToken": entity_token,
            "EntityId": entity_id,
            "EntityType": entity_type
        }), 200
    else:
        if login_request.status_code == 403:
            ban_info = login_request.json()
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
            error_info = login_request.json()
            error_message = error_info.get('errorMessage', 'An error occurred.')
            return jsonify({
                'Error': 'PlayFab Error',
                'Message': error_message
            }), login_request.status_code

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
        "REEL", "NII", "@here", "!", "JMAN", "PPPTIG", "CLEANINGBOT", "JANITOR", "K9",
        "H4PKY", "MOSA", "NIGGER", "NIGGA", "IHATENIGGERS", "@everyone", "TTT"
    ]
    if name not in BadNames:
        result = 0
    else:
        result = 2
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


@app.route("/api/photon", methods=["POST"])
def photonauth():
    data = request.get_json()
    if not data:
        return jsonify({"Error": "Bad Request", "Message": "Missing JSON body"}), 400

    Ticket = data.get("Ticket")
    Nonce = data.get("Nonce")
    TitleId = data.get("AppId")
    Platform = data.get("Platform")
    UserId = data.get("UserId")
    AppVersion = data.get("AppVersion")
    Token = data.get("Token")
    Username = data.get("Username")

    if not all([Ticket, Nonce, TitleId, Platform, UserId, AppVersion, Token, Username]):
        return jsonify({"Error": "Bad Request", "Message": "Missing one or more required fields"}), 400

    if Platform != 'Quest':
        return jsonify({
            "Error": "Invalid Platform",
            "Message": "Photon authentication is only supported for Quest platform"
        }), 403

    if Platform == "Steam":
        return jsonify({
            "Error": "Unsupported Platform",
            "Message": "Unable to authenticate your Oculus account from Steam. Please try again on Quest."
        }), 403

    if TitleId != title:
        return jsonify({
            "Error": "Invalid AppId",
            "Message": f"Invalid TitleId provided. Expected {title}, but got {TitleId}"
        }), 403

    print(f"Authentication request received from UserId: {UserId}, Platform: {Platform}, AppVersion: {AppVersion}, Username: {Username}")

    response = {
        "ResultCode": 1,
        "StatusCode": 200,
        "Message": "Authenticated with Photon successfully",
        "Result": 0,
        "UserId": UserId,
        "AppId": TitleId,
        "AppVersion": AppVersion,
        "Ticket": Ticket,
        "Token": Token,
        "Nonce": Nonce,
        "Platform": Platform,
        "Username": Username
    }

    return jsonify(response), 200

if __name__ == "__main__":
    print("Made by Nate")
    app.run(host="0.0.0.0", port=8080)
