from datetime import datetime
import profig
import pymongo
import os
import logging
import arrow

class Member:
    def __init__(self, **kwargs):
        logger = logging.getLogger("Member.__init__")

        self.email = kwargs.get("email", None)
        self.name = kwargs.get("name", None)
        self.registration_date = kwargs.get("registration_date", None)        
        self.config_path = os.path.join(os.getcwd(), "config.ini")

        logger.info("Opening a configuration from %s" % self.config_path)
        self.config = profig.Config(self.config_path)
        self.config.sync()

    @property
    def registration_date(self):
        return self._registration_date

    @registration_date.setter
    def registration_date(self, value):
        if type(value) is not str:
            self._registration_date = arrow.get(value).isoformat()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if value is not None:
            self._email = value.lower()

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "registrationDate": self.registration_date
        }

    def save(self):
        # TODO: Check if config is exists or not
        conn = pymongo.MongoClient(self.config["database.connection_string"])
        try:
            db = conn["gdg-surabaya"]
            member_exists = db.members.count({"email": self.email})
            member_exists = True if member_exists > 0 else False

            if not member_exists:
                db.members.insert({
                    "email": self.email,
                    "registrationDate": arrow.utcnow().datetime
                })
        finally:
            conn.close()

class Members:
    def __init__(self, **kwargs):
        logger = logging.getLogger("Members.__init__")
        self.members = kwargs.get("members", [])
        self.config_path = os.path.join(os.getcwd(), "config.ini")

        logger.info("Opening a configuration from %s" % self.config_path)
        self.config = profig.Config(self.config_path)
        self.config.sync()

    def save(self):
        for member in self.members:
            member.save()

    def find_all(self):
        conn = pymongo.MongoClient(self.config["database.connection_string"])
        try:
            db = conn["gdg-surabaya"]
            for member in db.members.find():
                yield Member(
                    email = member["email"] if "email" in member else "",
                    name = member["name"] if "name" in member else "",
                    registration_date = member["registrationDate"] if "registrationDate" in member else ""
                )
        finally:
            conn.close()