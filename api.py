from lib.listeners import MembersListener, MemberEmailsListener
from lib.middleware import RequireJSON, JSONTranslator
from falcon_cors import CORS
import falcon
import profig
import os

cfg = profig.Config(os.path.join(os.getcwd(), "config.ini"))
cfg.sync()

DEV = True if cfg["config.development"] == "true" else False

if not DEV:
    cors = CORS(
        allow_origins_list=["http://gdgsurabaya.org"], 
        allow_all_headers=True, 
        allow_all_methods=True
    )
else:
    cors = CORS(
        allow_all_origins=True, 
        allow_all_headers=True, 
        allow_all_methods=True
    )

api = falcon.API(middleware=[
    cors.middleware,
    RequireJSON(),
    JSONTranslator()
])
api.add_route("/members", MembersListener())
api.add_route("/members/{email}/emails",  MemberEmailsListener())