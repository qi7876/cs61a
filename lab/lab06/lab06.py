from typing import TypeVar, ClassVar


class Transaction:
    def __init__(self, id: int, before: int, after: int):
        self.id: int = id
        self.before: int = before
        self.after: int = after

    def changed(self):
        """Return whether the transaction resulted in a changed balance."""
        return self.before != self.after

    def report(self):
        """Return a string describing the transaction.

        >>> Transaction(3, 20, 10).report()
        '3: decreased 20->10'
        >>> Transaction(4, 20, 50).report()
        '4: increased 20->50'
        >>> Transaction(5, 50, 50).report()
        '5: no change'
        """
        msg = "no change"
        if self.changed():
            if self.before > self.after:
                msg = "decreased " + str(self.before) + "->" + str(self.after)
            else:
                msg = "increased " + str(self.before) + "->" + str(self.after)
        return str(self.id) + ": " + msg


class BankAccount:
    """A bank account that tracks its transaction history.

    >>> a = BankAccount('Eric')
    >>> a.deposit(100)    # Transaction 0 for a
    100
    >>> b = BankAccount('Erica')
    >>> a.withdraw(30)    # Transaction 1 for a
    70
    >>> a.deposit(10)     # Transaction 2 for a
    80
    >>> b.deposit(50)     # Transaction 0 for b
    50
    >>> b.withdraw(10)    # Transaction 1 for b
    40
    >>> a.withdraw(100)   # Transaction 3 for a
    'Insufficient funds'
    >>> len(a.transactions)
    4
    >>> len([t for t in a.transactions if t.changed()])
    3
    >>> for t in a.transactions:
    ...     print(t.report())
    0: increased 0->100
    1: decreased 100->70
    2: increased 70->80
    3: no change
    >>> b.withdraw(100)   # Transaction 2 for b
    'Insufficient funds'
    >>> b.withdraw(30)    # Transaction 3 for b
    10
    >>> for t in b.transactions:
    ...     print(t.report())
    0: increased 0->50
    1: decreased 50->40
    2: no change
    3: decreased 40->10
    """

    # *** YOU NEED TO MAKE CHANGES IN SEVERAL PLACES IN THIS CLASS ***

    def __init__(self, account_holder: str):
        self.balance: int = 0
        self.holder: str = account_holder
        self.transactions: list[Transaction] = []

    def add_transaction(self, before: int, after: int):
        if len(self.transactions) != 0:
            self.transactions.append(
                Transaction(self.transactions[-1].id + 1, before, after)
            )
        else:
            self.transactions.append(Transaction(0, before, after))

    def deposit(self, amount: int):
        """Increase the account balance by amount, add the deposit
        to the transaction history, and return the new balance.
        """
        self.add_transaction(self.balance, self.balance + amount)
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount: int):
        """Decrease the account balance by amount, add the withdraw
        to the transaction history, and return the new balance.
        """
        if amount > self.balance:
            self.add_transaction(self.balance, self.balance)
            return "Insufficient funds"

        self.add_transaction(self.balance, self.balance - amount)
        self.balance = self.balance - amount
        return self.balance


class Email:
    """An email has the following instance attributes:

    msg (str): the contents of the message
    sender (Client): the client that sent the email
    recipient_name (str): the name of the recipient (another client)
    """

    def __init__(self, msg: str, sender: "Client", recipient_name: str):
        self.msg: str = msg
        self.sender: Client = sender
        self.recipient_name: str = recipient_name


class Server:
    """Each Server has one instance attribute called clients that is a
    dictionary from client names to client objects.
    """

    def __init__(self):
        self.clients: dict[str, Client] = {}

    def send(self, email: Email):
        """Append the email to the inbox of the client it is addressed to.
        email is an instance of the Email class.
        """
        self.clients[email.recipient_name].inbox.append(email)

    def register_client(self, client: "Client"):
        """Add a client to the clients mapping (which is a
        dictionary from client names to client instances).
            client is an instance of the Client class.
        """
        self.clients[client.name] = client


class Client:
    """A client has a server, a name (str), and an inbox (list).

    >>> s = Server()
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> a.compose('Hello, World!', 'Bob')
    >>> b.inbox[0].msg
    'Hello, World!'
    >>> a.compose('CS 61A Rocks!', 'Bob')
    >>> len(b.inbox)
    2
    >>> b.inbox[1].msg
    'CS 61A Rocks!'
    >>> b.inbox[1].sender.name
    'Alice'
    """

    def __init__(self, server: Server, name: str):
        self.inbox: list[Email] = []
        self.server: Server = server
        self.name: str = name
        server.register_client(self)

    def compose(self, message: str, recipient_name: str):
        """Send an email with the given message to the recipient."""
        email = Email(message, self, recipient_name)
        self.server.send(email)


CoinT = TypeVar("CoinT", bound="Coin")


class Mint:
    """A mint creates coins by stamping on years.

    The update method sets the mint's stamp to Mint.present_year.

    >>> mint = Mint()
    >>> mint.year
    2024
    >>> dime = mint.create(Dime)
    >>> dime.year
    2024
    >>> Mint.present_year = 2104  # Time passes
    >>> nickel = mint.create(Nickel)
    >>> nickel.year     # The mint has not updated its stamp yet
    2024
    >>> nickel.worth()  # 5 cents + (80 - 50 years)
    35
    >>> mint.update()   # The mint's year is updated to 2104
    >>> Mint.present_year = 2179     # More time passes
    >>> mint.create(Dime).worth()    # 10 cents + (75 - 50 years)
    35
    >>> Mint().create(Dime).worth()  # A new mint has the current year
    10
    >>> dime.worth()     # 10 cents + (155 - 50 years)
    115
    >>> Dime.cents = 20  # Upgrade all dimes!
    >>> dime.worth()     # 20 cents + (155 - 50 years)
    125
    """

    present_year: ClassVar[int] = 2024

    def __init__(self):
        self.update()

    def create(self, coin: type[CoinT]) -> CoinT:
        return coin(self.year)

    def update(self):
        self.year: int = self.present_year


class Coin:
    cents: ClassVar[int]  # will be provided by subclasses, but not by Coin itself

    def __init__(self, year: int):
        self.year: int = year

    def worth(self) -> int:
        return self.cents + max(Mint.present_year - self.year - 50, 0)


class Nickel(Coin):
    cents: ClassVar[int] = 5


class Dime(Coin):
    cents: ClassVar[int] = 10
