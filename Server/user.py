import mysql.connector


class User:
    def __init__(self, connection : mysql.connector, username = None, token = None, invitation_code = None):
        self._connection = connection

        query = f"""SELECT * FROM UserData WHERE"""
        if username:
            query += f" username = '{username}';"
        elif token:
            query += f" token = '{token}';"
        elif invitation_code:
            query += f" invite_code = '{invitation_code}';"

        cursor = self._connection.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()[0]

        self.username = data["username"]
        self.hash = data["hash"]
        self.invited_by = data["was_invited_with"]
        self.invite_code = data["invite_code"]
        self.token = data["token"]
        self._money = data["money"]
        cursor.close()

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        self._money = value
        cursor = self._connection.cursor()
        query = f"UPDATE UserData SET money = {value} WHERE username = '{self.username}'"
        cursor.execute(query)
        cursor.close()

    @property
    def was_invited_by_user(self):
        return User(self._connection, None, None, self.invited_by)

    def __eq__(self, other):
        if type(other) != User:
            return False
        return other.username == self.username