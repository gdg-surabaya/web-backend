from lib.listeners import MembersListener
from lib.middleware import RequireJSON, JSONTranslator
from falcon_cors import CORS
import falcon

DEV = False

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