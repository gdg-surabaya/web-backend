import hashlib
import logging
import os
import pymongo
import arrow
import profig

class Verification:
    def __init__(self, **kwargs):
        logger = logging.getLogger("Verification.__init__")
        self.key = kwargs.get("key", None)
        self.config_path = os.path.join(os.getcwd(), "config.ini")

        logger.info("Opening a configuration from %s" % self.config_path)
        self.config = profig.Config(self.config_path)
        self.config.sync()

        self.salt = self.config["security.salt"]
    
    @property
    def key(self):
        if self._key is None:
            self.generate_key()
        return self._key
    
    @key.setter
    def key(self, value):
        self._key = value

    def generate_key(self, word):
        salted_word = "%s_%s" % (word, self.salt)
        salted_word = salted_word.encode("utf8")
        self.key = hashlib.sha256(salted_word).hexdigest()

    def save_key(self, member):
        conn = pymongo.MongoClient(self.config["database.connection_string"])
        try:
            client = conn["gdg-surabaya"]
            client.verifications.create_index("TTL", expireAfterSeconds=60*60*24*7)
            client.verifications.insert({
                "key": self.key,
                "owner": member.email,
                "isVerified": False,
                "TTL": arrow.utcnow().replace(days=+7).datetime
            })
        finally:
            conn.close()

    def verify(self):
        conn = pymongo.MongoClient(self.config["database.connection_string"])
        try:
            client = conn["gdg-surabaya"]
            client.verifications.update({"key": self.key}, {"$set":{"isVerified": True}})
        finally:
            conn.close()