import copy

import falcon

from ..model import Members, Member

class MembersListener:
    def on_get(self, req, res):
        members = Members().find_all()

        result = {"members":[]}
        for member in members:
            result["members"].append(member.to_dict())

        req.context["result"] = result
        res.status_code = falcon.HTTP_200

    def on_post(self, req, res):
        if "doc" not in req.context:
            raise falcon.HTTPBadRequest('Missing thing', 'A thing must be submitted in the request body.')
        data = copy.deepcopy(req.context["doc"])
        
        if "email" not in data:
            raise falcon.HTTPBadRequest("Cannot find email", "Email is not provided when you are requesting this API.")
        
        members = Members(members=[Member(email=data["email"])])
        members.save()

        req.context["result"] = {"status":{
            "code": "200",
            "message": "success"
        }}
        res.status_code = falcon.HTTP_200        
