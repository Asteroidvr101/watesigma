import requests
import random
from flask import Flask, jsonify, request

app = Flask(__name__)
title = ""
secretkey = ""
coems = {}
banned_users = {}

def authjh():
    return {"content-type": "application/json", "X-SecretKey": secretkey}

@app.route("/", methods=["POST", "GET"])
def no():
    return "yesnt"

@app.route('/api/PlayFabAuthentication', methods=["POST"])
def PlayFabAuthentication():
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
