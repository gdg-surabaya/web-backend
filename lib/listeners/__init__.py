from ..model import Members
import copy
import falcon

class MembersListener:
    def on_post(self, req, res):
        # body = req.get_param("email")
        # print(body)

        if "doc" not in req.context:
            raise falcon.HTTPBadRequest('Missing thing', 'A thing must be submitted in the request body.')
        data = copy.deepcopy(req.context["doc"])
        
        if "email" not in data:
            raise falcon.HTTPBadRequest("Cannot find email", "Email is not provided when you are requesting this API.")
        
        member = Members(email=data["email"])
        member.save()

        req.context["result"] = {"status":{
            "code": "200",
            "message": "success"
        }}
        res.status_code = falcon.HTTP_200        
