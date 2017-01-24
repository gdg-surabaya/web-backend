import copy
import os

import falcon
import requests
import profig

from jinja2 import Template
from ..model import Member, Verification

class MemberEmailsListener:
    def on_post(self, req, res, email):
        cfg = profig.Config(os.path.join(os.getcwd(), "config.ini"))
        cfg.sync()

        accepted_types = ["verification"]

        if "doc" not in req.context:
            raise falcon.HTTPBadRequest('Missing thing', 'A thing must be submitted in the request body.')
        data = copy.deepcopy(req.context["doc"])

        if "type" not in data:
            raise falcon.HTTPBadRequest("Cannot find type", "Type is not provided when you are requesting this API.")

        if data["type"] not in accepted_types:
            raise falcon.HTTPBadRequest("Type is not accepted", "The parameters provided inside the request is not listed from our list.")

        # Check if member is exists or not
        member = Member(email=email)
        if not member.exists:
            raise falcon.HTTPBadRequest("Cannot find email", "Cannot find email. You need to provide a correct email address.")
        
        # Preparing data to be sent to recipient
        email_data = {
            "from": "GDG Surabaya <noreply.verification@gdgsurabaya.org>",
            "to": [member.email]
        }

        if data["type"] == "verification":
            # Generate verification unique key
            verification = Verification()
            verification.generate_key(word=member.email)
            verification.save_key(member=member)

            verification_html = Template(open(os.path.join(os.getcwd(), "assets", "email-verification.html")).read())
            verification_html = verification_html.render(
                verification_address = "http://gdgsurabaya.org/verify/%s" % verification.key
            )           

            email_data.update({"subject": "GDG Surabaya email verification"})
            email_data.update({"html": verification_html})

        requests.post(
            "https://api.mailgun.net/v3/%s/messages" % cfg["mailgun.domain"],
            auth=("api", cfg["mailgun.api"]),
            files=[("inline", open(os.path.join(os.getcwd(), "assets", "logo.png"), "rb"))],
            data=email_data
        )

        req.context["result"] = {"status":{
            "code": "200",
            "message": "success"
        }}
        res.status_code = falcon.HTTP_200    