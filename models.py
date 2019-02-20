class Account():
    """
    name:名稱
    """

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Transaction():
    """
    from_account:從帳戶
    to_account:到帳戶
    amount:金額
    """

    def __init__(self, from_account, to_account, amount):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def __str__(self):
        return "{}轉帳給{}:{}".format(str(self.from_account), str(self.to_account), self.amount)


class AccountRelation():
    """
    account:帳戶
    relative_account:與其他帳戶的關係
        {
            account1: 100,
            account2: 200,
            account3: 500,
            account4: 300
        }
    """

    def __init__(self, account, relative_account):
        self.account = account
        self.relative_account = relative_account

    def get_total_amount(self):
        return sum([v for k, v in self.relative_account.items()])

    def __str__(self):
        return "{}:{}".format(str(self.account), str(self.relative_account))
