class LocalCache:
    def __init__(self) -> None:
        self._partners = {}

    def set_partner(self, user_id: int, partner_id: int) -> None:
        self._partners[user_id] = partner_id
        self._partners[partner_id] = user_id

    def get_partner(self, user_id: int) -> int:
        return self._partners.get(user_id)

