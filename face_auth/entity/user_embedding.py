class Embedding:
    """Entity class for user embedding"""

    def __init__(self, UUID: str = None, user_embed=None) -> None:
        self.UUID = UUID
        self.user_embed = user_embed

    def to_dict(self) -> dict:
        return self.__dict__

    def __str__(self) -> str:
        return str(self.to_dict())
