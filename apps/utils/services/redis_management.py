import redis
import json


class RedisHandler(object):
    def __init__(self, url):
        self.url = url
        self.handle = self.load_handler()

    def load_handler(self):
        """
        loads the handler
        in order to manage
        the handler, if there's an error
        it won't return nothing.
        """
        result = {}
        try:
            result = redis.from_url(self.url)

        except Exception:
            pass
        return result

    def clean_cache(self):
        """
        deletes all information
        stored in memory, this is done
        for debugging purposes.
        """
        for k in self.handle.keys():
            self.handle.delete(k)

    def serialize(self, value):
        """
        serializes the value,
        typically should be taken
        from redis as an encoded
        str.
        """
        return json.loads(value.decode() if value else {"empty": "empty"})

    def deserialize(self, value):
        """
        deserializes the value
        to be inserted in
        redis which is
        converted to json.

        :params:
            deserialize: object
        :return: json
        """
        return json.dumps(value if value else {"empty": "empty"})

    def set_item(self, key, item):
        """
        sets the item with the given key
        """
        result = {}
        try:
            if isinstance(self.handle, dict):
                self.handle[key] = item

            else:
                deserialized = self.deserialize(item)
                self.handle.set(key, deserialized)
            result["status"] = True

        except Exception as X:
            result["status"] = False
            result["error"] = X

        return result

    def get_item(self, key):
        """
        gets the item with the given key
        """
        result = {}
        try:
            value = self.handle.get(key)
            if value:
                result['data'] = (self.serialize(value)
                                  if not isinstance(self.handle, dict)
                                  else value)
                result["status"] = True
            else:
                result["status"] = False

        except Exception as X:
            result["status"] = False
            result["error"] = X

        return result

    def delete_item(self, key):
        """
        deletes the item with the
        given key.
        :param: key: str
        returns: dict
        """
        result = {}
        try:
            if isinstance(self.handle, dict):
                self.handle.__delitem__(key)
            else:
                self.handle.delete(key)
            result["status"] = True

        except Exception as X:
            result["status"] = False
            result["error"] = X

        return result

    def set_qr_validator_jwt(self, key, jwt_data):
        """
        sets the jwt for the qr validator
        that uses it in order to access 
        to it later on for reading the qr.

        :params:
            key: key identifier for the qr reader.
            this is their uuid
            jwt_data: this is the response coming
            from the remote validator service: dict.
        :returns: dict.
        """
        key = f"{key}_jwt"
        result = self.set_item(key=key, item=jwt_data)
        return result

    def get_qr_validator_jwt(self, key):
        """
        gets the jwt for the qr validator
        that uses it in order to access 
        to it later on for reading the qr.

        :params:
            key: key identifier for the qr reader.
            this is their token
        :returns: dict.
        """
        key = f"{key}_jwt"
        result = self.get_item(key=key)
        return result

  