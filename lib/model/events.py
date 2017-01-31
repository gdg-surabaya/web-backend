import logging
import os

import arrow
import profig
import pymongo

class Event:
    def __init__(self, **kwargs):
        logger = logging.getLogger("Event.__init__")

        self.title = kwargs.get("title", None)
        self.description = kwargs.get("description", None)
        self.date = kwargs.get("date", None)
        self.start_time = kwargs.get("start_time", None)
        self.end_time = kwargs.get("end_time", None)
        self.location_name = kwargs.get("location_name", None)
        self.can_register = kwargs.get("can_register", None)
        self.registration_url = kwargs.get("registration_url", None)
        
        self.config_path = os.path.join(os.getcwd(), "config.ini")

        logger.info("Opening a configuration from %s" % self.config_path)
        self.config = profig.Config(self.config_path)
        self.config.sync()

    @property
    def date(self):
        return arrow.get(self._date).isoformat()
    
    @date.setter
    def date(self, value):
        self._date = None
        if value is not None:
            self._date = arrow.get(value).to("utc").datetime

    @property
    def start_time(self):
        return arrow.get(self._start_time).isoformat()
    
    @start_time.setter
    def start_time(self, value):
        self._start_time = None
        if value is not None:
            self._start_time = arrow.get(value).to("utc").datetime

    @property
    def end_time(self):
        return arrow.get(self._end_time).isoformat()
    
    @end_time.setter
    def end_time(self, value):
        self._end_time = None
        if value is not None:
            self._end_time = arrow.get(value).to("utc").datetime

    def to_dict(self):
        return{
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "startTime": self.start_time,
            "endTime": self.end_time,
            "location":{"name": self.location_name},
            "canRegister": self.can_register,
            "registrationURL": self.registration_url
        }

    def save(self):
        # TODO: Check if config is exists or not
        conn = pymongo.MongoClient(self.config["database.connection_string"])
        try:
            document = self.to_dict()
            document.update({"insertTime": arrow.utcnow().datetime})
            document.update({"isActive": True})
    
            db = conn["gdg-surabaya"]
            db.events.insert(document)
        finally:
            conn.close()

class Events:
    def __init__(self, **kwargs):
        logger = logging.getLogger("Events.__init__")
        self.events = kwargs.get("events", [])
        self.config_path = os.path.join(os.getcwd(), "config.ini")

        logger.info("Opening a configuration from %s" % self.config_path)
        self.config = profig.Config(self.config_path)
        self.config.sync()

    def save(self):
        for event in self.events:
            event.save()
    
    def find_all(self):
        conn = pymongo.MongoClient(self.config["database.connection_string"])
        try:
            db = conn["gdg-surabaya"]
            for event in db.events.find():
                yield Event(
                    title = event["title"],
                    description = event["description"],
                    date = event["date"],
                    start_time = event["startTime"],
                    end_time = event["endTime"],
                    location_name = event["location"]["name"],
                    can_register = event["canRegister"],
                    registration_url = event["registrationURL"]                   
                )
        finally:
            conn.close() 