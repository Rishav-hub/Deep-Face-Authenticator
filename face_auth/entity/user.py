import uuid


class User:
    def __init__(
        self,
        Name: str,
        username: str,
        email_id: str,
        ph_no: str,
        password1: str,
        password2: str,
        uuid_: str = None,
    ):
        self.Name = Name
        self.username = username
        self.email_id = email_id
        self.ph_no = ph_no
        self.password1 = password1
        self.password2 = password2
        self.uuid_ = uuid_
        if not self.uuid_:
            self.uuid_ = str(uuid.uuid4()) + str(uuid.uuid4())[0:4]

    def to_dict(self) -> dict:
        return self.__dict__

    def __str__(self) -> str:
        return str(self.to_dict())
