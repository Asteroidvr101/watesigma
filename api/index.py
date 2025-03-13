import requests
import random
from flask import Flask, jsonify, request

app = Flask(__name__)
title = "7AF94"
secretkey = "GBIPB74594RF9UDYHIAKASEJ1WG66KWWF4FAPKJK1WYZCC94S7" #idk why it said secfret
coems = {} # bro why does this have ;


def authjh():
    return {"content-type": "application/json","X-SecretKey": secretkey}

@app.route("/", methods=["POST", "GET"])
def no():
    return "Wassup Fucking Skidder :sob:"

@app.route('/api/PlayFabAuthentication', methods=['POST'])
def PlayFabAuthentication():
    data = request.get_json()
    
    print(data)

    CustomId: str = data.get("CustomId", "Null")
    Nonce: str = data.get("Nonce", "Null")
    OculusId: str = data.get("OculusId", "Null")
    Platform: str = data.get("Platform", "Null")

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
            return jsonify({"Message": "Failed to link Custom ID."}), 400
    else:
        try:
            error_info = BLAH.json().get("error")  # Get the details of the error if available
            if error_info and "banned" in error_info.get("message", "").lower():
                # If the error message contains information about a ban
                return jsonify({
                    "Message": "You are banned from the game.",
                    "Reason": error_info.get("message")
                }), 403
            else:
                return jsonify({
                    "Message": "Authentication failed.",
                    "Reason": error_info.get("message", "Unknown error.")
                }), 403
        except (ValueError, KeyError) as e:
            # Log the parsing error if needed
            return jsonify({"Message": "An error occurred while processing the response."}), 500
                playfab_id = request.json.get("PlayFabId")

    # Check if the user is in the cache and if they are banned
    if playfab_id in coems:
        if coems[playfab_id].get('is_banned', False):
            return jsonify({"Message": "You are banned from joining the lobby."}), 403

    # If they are not banned, allow them to join the lobby
    return jsonify({"Message": "Successfully joined the lobby."}), 200

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

@app.route("/cbfn", methods=["POST","GET"])
def cfbn():
    name = request.args.get('name')
    code = request.args.get('code')
    BadNames = [
        "KKK", "PENIS", "NIGG", "NEG", "NIGA", "MONKEYSLAVE", "SLAVE", "FAG", 
        "NAGGI", "TRANNY", "QUEER", "KYS", "DICK", "PUSSY", "VAGINA", "BIGBLACKCOCK", 
        "DILDO", "HITLER", "KKX", "XKK", "NIGA", "NIGE", "NIG", "NI6", "PORN", 
        "JEW", "JAXX", "TTTPIG", "SEX", "COCK", "CUM", "FUCK", "PENIS", "DICK", 
        "ELLIOT", "JMAN", "K9", "NIGGA", "TTTPIG", "NICKER", "NICKA", 
        "REEL", "NII", "@here", "!", " ", "JMAN", "PPPTIG", "CLEANINGBOT", "JANITOR", "K9", 
        "H4PKY", "MOSA", "NIGGER", "NIGGA", "IHATENIGGERS", "@everyone", "TTT"
    ];
    if name not in BadNames:result = 0
    if code not in BadNames:result = 0
    else: result = 2
    return jsonify({"Message":"the name thingy worked!","Name":name,"Result":result})

@app.route("/gaa", methods=["POST", "GET"])
def gaa():
    getjson = request.get_json()["FunctionResult"]
    return jsonify(getjson)

@app.route("/saa", methods=["POST", "GET"])
def saa():
    getjson = request.get_json()["FunctionResult"]
    return jsonify(getjson) #qwizx did this on purpose bro i swear

@app.route("/grn", methods=["POST", "GET"])
def grn():
    return jsonify({"result": f"pluh!{randoms.randint(1000, 9999)}"})

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
    if TitleId != '1B1323':
        return jsonify({'Error': 'Bad request', 'Message': 'Invalid titleid!'}), 403
    if Platform != 'Quest':
        return jsonify({'Error': 'Bad request', 'Message': 'Invalid platform!'}), 403
    return jsonify({"ResultCode":1, "StatusCode":200, "Message":"authed with photon",
        "Result": 0,
        "UserId": UserId,
        "AppId":TitleId,
        "AppVersion":AppVersion,
        "Ticket":Ticket,
        "Token":Token,
        "Nonce":Nonce,
        "Platform":Platform,
        "Username":Username}), 200



if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80)
