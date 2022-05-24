from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

malwares = [
    {
        "name" : "spyfocus.js",
        "type" : "adware",
        "media" : "url",
    },
    {
        "name" : "greencard.zip",
        "type" : "trojan",
        "media" : "zip",
    },
    {
        "name" : "credit_card.rar",
        "type" : "trojan",
        "media" : "zip",
    },    
    {
        "name" : "system35.dll",
        "type" : "virus",
        "media" : "exe",
    },  
    {
        "name" : "registry_mode.bat",
        "type" : "worm",
        "media" : "msi",
    }
]

class Malware(Resource):
        def get (self, name):
            for malware in malwares:
                if (name == malware["name"]):
                    return malware, 200
            return "Marlware not found", 404

        def post (self, name):
            parser = reqparse.RequestParser()
            parser.add_argument("type")
            parser.add_argument("media")
            args = parser.parse_args()

            for malware in malwares:
                if(name == malware["name"]):
                    return"Malware with name {} already exits".format(name), 400
            malware = {
                "name" : name,
                "type" : args["type"],
                "media" : args["media"]
            }

            malwares.append(malware)
            return malware, 201

        def put (self, name):
            parser = reqparse.RequestParser()
            parser.add_argument("type")
            parser.add_argument("media")
            args = parser.parse_args()

            for malware in malwares:
                if (name==malware["name"]):
                    malware["type"] = args["type"]
                    malware["media"] = args["media"]
                    return malware, 200

            malware = {
                "name" : name,
                "type" : args["type"],
                "media" : args["media"]
            }
    
            malwares.append(malware)
            return malware, 201

        def delete (self, name):
            global malwares
            malwares = [malware for malware in malwares if malware["name"] != name]
            return "{} is deleted.".format(name), 200
        
api.add_resource(Malware, "/malware/<string:name>")
app.run(debug = True) #enable flask to reload after a change, only develoing mode.
