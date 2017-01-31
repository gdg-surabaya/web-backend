from ..model import Events, Event

import falcon
import copy

class EventsListener:
    def on_get(self, req, res):
        events = Events().find_all()

        result = {"events":[]}
        for event in events:
            result["events"].append(event.to_dict())
        
        req.context["result"] = result
        res.status_code = falcon.HTTP_200

    def on_post(self, req, res):
        if "doc" not in req.context:
            raise falcon.HTTPBadRequest('Missing thing', 'A thing must be submitted in the request body.')
        data = copy.deepcopy(req.context["doc"])

        if "title" not in data:
            raise falcon.HTTPBadRequest("Cannot find title", "Title is not provided when you are requesting this API.")

        if "description" not in data:
            raise falcon.HTTPBadRequest("Cannot find description", "Description is not provided when you are requesting this API.")

        if "date" not in data:
            raise falcon.HTTPBadRequest("Cannot find date", "Date is not provided when you are requesting this API.")
        
        if "startTime" not in data:
            raise falcon.HTTPBadRequest("Cannot find startTime", "Start time is not provided when you are requesting this API.")

        if "endTime" not in data:
            raise falcon.HTTPBadRequest("Cannot find endTime", "End time is not provided when you are requesting this API.")

        if "location" not in data:
            raise falcon.HTTPBadRequest("Cannot find location", "Location is not provided when you are requesting this API.")

        if "name" not in data["location"]:
            raise falcon.HTTPBadRequest("Cannot find name in location", "Location name is not provided when you are requesting this API.")

        if "canRegister" not in data:
            raise falcon.HTTPBadRequest("Cannot find canRegister", "Can register is not provided when you are requesting this API.")

        if "registrationURL" not in data:
            raise falcon.HTTPBadRequest("Cannot find registrationURL", "Registertration URL is not provided when you are requesting this API.")
        
        events = Events(events=[Event(
            title=data["title"],
            description=data["description"],
            date=data["date"],
            start_time=data["startTime"],
            end_time=data["endTime"],
            location_name=data["location"]["name"],
            can_register=data["canRegister"],
            registration_url=data["registrationURL"]
        )])
        events.save()

        req.context["result"] = {"status":{
            "code": "200",
            "message": "success"
        }}
        res.status_code = falcon.HTTP_200  