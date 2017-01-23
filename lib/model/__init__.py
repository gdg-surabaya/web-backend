import profig
import pymongo
import os
import logging
import arrow

class Members:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger("Members.__init__")
        self.email = kwargs.get("email", None)
        self.config_path = os.path.join(os.getcwd(), "config.ini")

        self.logger.info("Opening a configuration from %s" % self.config_path)
        self.config = profig.Config(self.config_path)
        self.config.sync()
        
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value.lower()

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