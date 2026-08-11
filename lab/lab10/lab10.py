############## You do not need to understand any of this code!
import base64
from typing import Callable, Final, TypeAlias, cast, override
ob = "CmRlZiBhZGRpdGlvbihleHByKToKICAgIGRpdmlkZW5kID0gZXhwci5maXJzdAogICAgZXhwciA9IGV4cHIucmVzdAogICAgd2hpbGUgZXhwciAhPSBuaWw6CiAgICAgICAgZGl2aXNvciA9IGV4cHIuZmlyc3QKICAgICAgICBkaXZpZGVuZCArPSBkaXZpc29yCiAgICAgICAgZXhwciA9IGV4cHIucmVzdAogICAgcmV0dXJuIGRpdmlkZW5kCgpkZWYgc3VidHJhY3Rpb24oZXhwcik6CiAgICBkaXZpZGVuZCA9IGV4cHIuZmlyc3QKICAgIGV4cHIgPSBleHByLnJlc3QKICAgIHdoaWxlIGV4cHIgIT0gbmlsOgogICAgICAgIGRpdmlzb3IgPSBleHByLmZpcnN0CiAgICAgICAgZGl2aWRlbmQgLT0gZGl2aXNvcgogICAgICAgIGV4cHIgPSBleHByLnJlc3QKICAgIHJldHVybiBkaXZpZGVuZAoKZGVmIG11bHRpcGxpY2F0aW9uKGV4cHIpOgogICAgZGl2aWRlbmQgPSBleHByLmZpcnN0CiAgICBleHByID0gZXhwci5yZXN0CiAgICB3aGlsZSBleHByICE9IG5pbDoKICAgICAgICBkaXZpc29yID0gZXhwci5maXJzdAogICAgICAgIGRpdmlkZW5kICo9IGRpdmlzb3IKICAgICAgICBleHByID0gZXhwci5yZXN0CiAgICByZXR1cm4gZGl2aWRlbmQKCmRlZiBkaXZpc2lvbihleHByKToKICAgIGRpdmlkZW5kID0gZXhwci5maXJzdAogICAgZXhwciA9IGV4cHIucmVzdAogICAgd2hpbGUgZXhwciAhPSBuaWw6CiAgICAgICAgZGl2aXNvciA9IGV4cHIuZmlyc3QKICAgICAgICBkaXZpZGVuZCAvPSBkaXZpc29yCiAgICAgICAgZXhwciA9IGV4cHIucmVzdAogICAgcmV0dXJuIGRpdmlkZW5kCg=="
exec(base64.b64decode(ob.encode("ascii")).decode("ascii"))
##############
Number = int | float
Operator: TypeAlias = Callable[["Pair"], Number]
SchemeExpression: TypeAlias = "Pair | int | float | bool | str"
EvaluationResult: TypeAlias = "Number | bool | str | Operator"

# These functions are created by the exec call above. The declarations make
# their signatures visible to static type checkers without changing runtime
# behavior.
addition = cast(Operator, globals()["addition"])
subtraction = cast(Operator, globals()["subtraction"])
multiplication = cast(Operator, globals()["multiplication"])
division = cast(Operator, globals()["division"])

def calc_eval(exp: SchemeExpression) -> EvaluationResult:
    """
    >>> calc_eval(Pair("define", Pair("a", Pair(1, nil))))
    'a'
    >>> calc_eval("a")
    1
    >>> calc_eval(Pair("+", Pair(1, Pair(2, nil))))
    3
    """
    if isinstance(exp, Pair):
        operator = exp.first # UPDATE THIS FOR Q2, e.g (+ 1 2), + is the operator
        operands = exp.rest # UPDATE THIS FOR Q2, e.g (+ 1 2), 1 and 2 are operands
        if not isinstance(operator, str):
            raise TypeError("operator must be a symbol")
        if operator == 'and': # and expressions
            return eval_and(operands)
        elif operator == 'define': # define expressions
            return eval_define(operands)
        else: # Call expressions
            if not isinstance(operands, Pair):
                raise TypeError("call expression requires operands")
            procedure = calc_eval(operator)
            if not callable(procedure):
                raise TypeError(f"{operator} is not a procedure")
            return calc_apply(procedure, operands) # UPDATE THIS FOR Q2, what is type(operator)?
    elif isinstance(exp, (int, float)):   # Numbers and booleans
        return exp
    elif exp in OPERATORS:   # Looking up procedures
        return OPERATORS[exp]
    elif exp in bindings: # CHANGE THIS CONDITION FOR Q4 where are variables stored?
        return bindings[exp] # UPDATE THIS FOR Q4, how do you access a variable?
    raise NameError(f"unknown identifier: {exp}")

def calc_apply(op: Operator, args: "Pair") -> Number:
    return op(args)

def floor_div(args: "Pair") -> Number:
    """
    >>> floor_div(Pair(100, Pair(10, nil)))
    10
    >>> floor_div(Pair(5, Pair(3, nil)))
    1
    >>> floor_div(Pair(1, Pair(1, nil)))
    1
    >>> floor_div(Pair(5, Pair(2, nil)))
    2
    >>> floor_div(Pair(23, Pair(2, Pair(5, nil))))
    2
    >>> calc_eval(Pair("//", Pair(4, Pair(2, nil))))
    2
    >>> calc_eval(Pair("//", Pair(100, Pair(2, Pair(2, Pair(2, Pair(2, Pair(2, nil))))))))
    3
    >>> calc_eval(Pair("//", Pair(100, Pair(Pair("+", Pair(2, Pair(3, nil))), nil))))
    20
    """
    "*** YOUR CODE HERE ***"
    initial_value = calc_eval(args.first)
    if not isinstance(initial_value, (int, float)):
        raise TypeError("// operands must be numbers")
    result: Number = initial_value
    rest = args.rest

    while isinstance(rest, Pair):
        divisor = calc_eval(rest.first)
        if not isinstance(divisor, (int, float)):
            raise TypeError("// operands must be numbers")
        result = result // divisor
        rest = rest.rest

    return result

scheme_t = True   # Scheme's #t
scheme_f = False  # Scheme's #f

def eval_and(expressions: "Pair | Nil") -> EvaluationResult:
    """
    >>> calc_eval(Pair("and", Pair(1, nil)))
    1
    >>> calc_eval(Pair("and", Pair(False, Pair("1", nil))))
    False
    >>> calc_eval(Pair("and", Pair(1, Pair(Pair("//", Pair(5, Pair(2, nil))), nil))))
    2
    >>> calc_eval(Pair("and", Pair(Pair('+', Pair(1, Pair(1, nil))), Pair(3, nil))))
    3
    >>> calc_eval(Pair("and", Pair(Pair('-', Pair(1, Pair(0, nil))), Pair(Pair('/', Pair(5, Pair(2, nil))), nil))))
    2.5
    >>> calc_eval(Pair("and", Pair(0, Pair(1, nil))))
    1
    >>> calc_eval(Pair("and", nil))
    True
    """
    "*** YOUR CODE HERE ***"
    if isinstance(expressions, Nil):
        return scheme_t

    val = calc_eval(expressions.first)
    if val is scheme_f:
        return scheme_f
    if isinstance(expressions.rest, Nil):
        return val
    return eval_and(expressions.rest)

bindings: dict[str, EvaluationResult] = {}

def eval_define(expressions: "Pair | Nil") -> str:
    """
    >>> eval_define(Pair("a", Pair(1, nil)))
    'a'
    >>> eval_define(Pair("b", Pair(3, nil)))
    'b'
    >>> eval_define(Pair("c", Pair("a", nil)))
    'c'
    >>> calc_eval("c")
    1
    >>> calc_eval(Pair("define", Pair("d", Pair("//", nil))))
    'd'
    >>> calc_eval(Pair("d", Pair(4, Pair(2, nil))))
    2
    """
    "*** YOUR CODE HERE ***"
    if isinstance(expressions, Nil):
        raise TypeError("define requires a name and value")
    name = expressions.first
    if not isinstance(name, str):
        raise TypeError("define name must be a symbol")
    if not isinstance(expressions.rest, Pair):
        raise TypeError("define requires a value")

    bindings[name] = calc_eval(expressions.rest.first)
    return name

OPERATORS = { "//": floor_div, "+": addition, "-": subtraction, "*": multiplication, "/": division }

class Pair:
    """A pair has two instance attributes: first and rest. rest must be a Pair or nil

    >>> s = Pair(1, Pair(2, nil))
    >>> s
    Pair(1, Pair(2, nil))
    >>> print(s)
    (1 2)
    >>> print(s.map(lambda x: x+4))
    (5 6)
    """
    def __init__(self, first: SchemeExpression, rest: "Pair | Nil") -> None:
        self.first: SchemeExpression = first
        self.rest: Pair | Nil = rest

    @override
    def __repr__(self) -> str:
        return 'Pair({0}, {1})'.format(repr(self.first), repr(self.rest))

    @override
    def __str__(self) -> str:
        s = '(' + str(self.first)
        rest = self.rest
        while isinstance(rest, Pair):
            s += ' ' + str(rest.first)
            rest = rest.rest
        if rest is not nil:
            s += ' . ' + str(rest)
        return s + ')'

    def __len__(self) -> int:
        n, rest = 1, self.rest
        while isinstance(rest, Pair):
            n += 1
            rest = rest.rest
        if rest is not nil:
            raise TypeError('length attempted on improper list')
        return n

    @override
    def __eq__(self, p: object) -> bool:
        if not isinstance(p, Pair):
            return False
        return self.first == p.first and self.rest == p.rest

    def map(self, fn: Callable[[SchemeExpression], SchemeExpression]) -> "Pair":
        """Return a Scheme list after mapping Python function FN to SELF."""
        mapped = fn(self.first)
        return Pair(mapped, self.rest.map(fn))

class Nil:
    """The empty list"""

    @override
    def __repr__(self) -> str:
        return 'nil'

    @override
    def __str__(self) -> str:
        return '()'

    def __len__(self) -> int:
        return 0

    def map(self, fn: Callable[[SchemeExpression], SchemeExpression]) -> "Nil":
        del fn
        return self

nil: Final = Nil()
