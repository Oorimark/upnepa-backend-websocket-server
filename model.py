import json


class FILE_STORAGE:
    """ OTP SERVICE STORAGE WORKER: store pending otp """

    file_name = 'temp.db'

    def __init__(self):
        if not (self.read_file()):
            self.write_file([])

    def read_file(self):
        with open(self.file_name) as db:
            data = db.read()
            return json.loads(data) if data else data

    def write_file(self, updated_content):
        with open(self.file_name, 'w') as db:
            db.write(json.dumps(updated_content, indent=5))

    def save_data(self, data):
        db = self.read_file()
        db.append(data)
        self.write_file(db)  # update db

    def delete_data(self, otp: int):
        db = self.read_file()
        updated_content = filter(lambda data: data['otp'] != otp, db)
        new_updated_content_bucket = list()
        for content in updated_content:
            new_updated_content_bucket.append(content)
        self.write_file(new_updated_content_bucket)

    def find_otp(self, otp: int) -> dict:
        db = self.read_file()
        for data in db:
            if data['otp'] == otp:
                return data

    def fetch(self) -> dict:
        db = self.read_file()
        return db[-1]

    def clear(self):
        with open(self.file_name, 'w') as db:
            db.write(json.dumps('[]', indent=4))
