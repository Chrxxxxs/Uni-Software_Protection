from z3 import *
from random import choice, getrandbits

x = BitVec("x", 64)
y = BitVec("y", 64)
z = BitVec("z", 64)

VARIABLES = [("x", x), ("y", y), ("z", z)]
OPERATORS = [
	("+", lambda left, right: left + right),
	("-", lambda left, right: left - right),
	("*", lambda left, right: left * right),
	("^", lambda left, right: left ^ right),
	("&", lambda left, right: left & right),
	("|", lambda left, right: left | right),
]


def leaf():
	if choice((True, False)):
		return choice(VARIABLES)

	value = getrandbits(64)
	return str(value), BitVecVal(value, 64)


def build_term(depth):
	if depth <= 0 or choice((True, False)):
		return leaf()

	left_string, left_expr = build_term(depth - 1)
	right_string, right_expr = build_term(depth - 1)
	operator, operator_expr = choice(OPERATORS)
	return f"({left_string} {operator} {right_string})", operator_expr(left_expr, right_expr)


def prove_opaque(predicate):
	solver = Solver()
	solver.add(predicate)
	if solver.check() == unsat:
		return True

	solver = Solver()
	solver.add(Not(predicate))
	return solver.check() == unsat


def build_candidate():
	template = choice(
		(
			"self_xor",
			"self_and",
			"self_or",
			"self_add",
			"self_sub",
			"self_mul",
			"zero_and",
			"zero_xor",
			"commutative",
			"associative",
		)
	)

	if template == "self_xor":
		term_string, term_expr = build_term(2)
		return f"({term_string} ^ {term_string}) == 0", (term_expr ^ term_expr) == BitVecVal(0, 64)

	if template == "self_and":
		term_string, term_expr = build_term(2)
		return f"({term_string} & {term_string}) != {term_string}", (term_expr & term_expr) != term_expr

	if template == "self_or":
		term_string, term_expr = build_term(2)
		return f"({term_string} | {term_string}) == {term_string}", (term_expr | term_expr) == term_expr

	if template == "self_add":
		term_string, term_expr = build_term(2)
		return f"({term_string} + 0) == {term_string}", (term_expr + BitVecVal(0, 64)) == term_expr

	if template == "self_sub":
		term_string, term_expr = build_term(2)
		return f"({term_string} - 0) == {term_string}", (term_expr - BitVecVal(0, 64)) == term_expr

	if template == "self_mul":
		term_string, term_expr = build_term(2)
		return f"({term_string} * 1) == {term_string}", (term_expr * BitVecVal(1, 64)) == term_expr

	if template == "zero_and":
		term_string, term_expr = build_term(2)
		return f"({term_string} & 0) != 0", (term_expr & BitVecVal(0, 64)) != BitVecVal(0, 64)

	if template == "zero_xor":
		term_string, term_expr = build_term(2)
		return f"({term_string} ^ 0) == {term_string}", (term_expr ^ BitVecVal(0, 64)) == term_expr

	left_string, left_expr = build_term(1)
	right_string, right_expr = build_term(1)
	operator, operator_expr = choice((OPERATORS[0], OPERATORS[3], OPERATORS[4], OPERATORS[5]))

	if template == "commutative":
		return (
			f"({left_string} {operator} {right_string}) == ({right_string} {operator} {left_string})",
			operator_expr(left_expr, right_expr) == operator_expr(right_expr, left_expr),
		)

	a_string, a_expr = build_term(1)
	b_string, b_expr = build_term(1)
	c_string, c_expr = build_term(1)

	return (
		f"(({a_string} {operator} {b_string}) {operator} {c_string}) == ({a_string} {operator} ({b_string} {operator} {c_string}))",
		operator_expr(operator_expr(a_expr, b_expr), c_expr) == operator_expr(a_expr, operator_expr(b_expr, c_expr)),
	)


def main():
	unique_opaque_predicates = []
	seen_predicates = set()
	attempts = 0

	while len(unique_opaque_predicates) < 10 and attempts < 1000:
		attempts += 1
		predicate_string, predicate_expr = build_candidate()
		if predicate_string in seen_predicates:
			continue
		if not prove_opaque(predicate_expr):
			continue

		seen_predicates.add(predicate_string)
		unique_opaque_predicates.append(predicate_string)

	if len(unique_opaque_predicates) < 10:
		raise RuntimeError("failed to generate 10 opaque predicates")

	for index, opaque_predicate in enumerate(unique_opaque_predicates):
		print(f"opaque predicate {index}: {opaque_predicate}")


if __name__ == "__main__":
	main()