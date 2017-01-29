from ..model.verification import Verification
import falcon

class VerificationListener:
    def on_patch(self, req, res, key):
        """ Ignore data that sent from requester, just focus on its key """
        verification = Verification(key=key)
        verification.verify()

        req.context["result"] = {"status":{
            "code": "200",
            "message": "success"
        }}
        res.status_code = falcon.HTTP_200  