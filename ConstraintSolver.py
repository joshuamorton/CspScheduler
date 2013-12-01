from collections import deque

"""
	Class to represent a constraint. Tracks the variables involved.
	Can determine whether a map of variables to values satisfies this constraint.
"""
class Constraint:
	"""
	Args:
		variables (list<Variable>): all variables involved in this constraint
		test_satisfied (function): a function that declares the constraint satisfied or not, takes in a  map of variables to values
		**extras: any extra information that should be given to the test_satisfies function
	"""
	def __init__(self, variables, test_satisfied, **extras):
		self.variables = variables
		self.test_satisfied = test_satisfied
		self.extras = extras
		for variable in self.variables:
			variable.add_constraint(self)
	
	"""
	Determines whether this constraint is satisfied by the given assignment

	Args:
		value_map (dictionary<Variable, ?>): a dictionary with variables and their assigned values, no unassigned variables
	Returns:
		boolean
		True if the constraint is satisfied with these values, false otherwise
	"""
	def is_satisfied(self, value_map):
		remove_variables = []
		for variable in value_map:
			if variable not in self.variables:
				remove_variables.append(variable)
		for variable in remove_variables:
			del value_map[variable]
		return self.test_satisfied(self.variables, value_map, self.extras)


"""
	Class to represent a variable. Has data, value, relevant constraints, conlfict set, and a domain.
"""
class Variable:
	"""
	Args:
		data (?): the data for this variable
		domain (list<?>): a list of values that this variable can be assigned
	"""
	def __init__(self, data, domain):
		self.data = data
		self.domain = domain
		self.constraints = []
		self.conflict_set = set([])
		self.value = None
		self.assigned = False

	"""
	Adds a constraint to the list of relevant constraints for this variable

	Args:
		constraint (Constraint): a constraint involving this variable
	"""
	def add_constraint(self, constraint):
		self.constraints.append(constraint)

	def add_conflict(self, variable):
		self.conflict_set.add(variable)

	def add_conflicts(self, other_set):
		self.conflict_set = self.conflict_set.union(other_set)
		if self in self.conflict_set:
			self.conflict_set.remove(self)

	def set_value(self, value):
		self.value = value
		self.assigned = True

	def clear_value(self):
		self.value = None
		self.assigned = False

	def __str__(self):
		return str(self.data)

	def __repr__(self):
		return str(self.data)


class ConstraintSatisfactionProblem:
	def __init__(self, variables, constraints):
		self.variables = variables
		self.unary_constraints = []
		self.binary_constraints = []
		self.nary_constraints = []
		for constraint in constraints:
			if len(constraint.variables) == 1:
				self.unary_constraints.append(constraint)
			elif len(constraint.variables) == 2:
				self.binary_constraints.append(constraint)
			else:
				self.nary_constraints.append(constraint)

	def generate_assignment(self):
		solution = {}
		for variable in self.variables:
			solution[variable] = variable.value
		return solution

	def is_complete(self):
		for variable in self.variables:
			if not variable.assigned:
				return False
		return True

	def solve(self):
		# Removes unary constraints, preprocesses with ac3, and then uses recursive backtracking
		# Will return False, None, or [False, ...] respectively if failure
		if not self.remove_unary() or self.make_inferences() is None or not self.backtracking_search()[0]:
			return None
		return self.generate_assignment()

	def remove_unary(self):
		for constraint in self.unary_constraints:
			variable = constraint.variables[0]
			for value in variable.domain:
				if not constraint.is_satisfied({variable: value}):
					variable.domain.remove(value)
					if not variable.domain:
						return False
		return True

	def remove_inferences(self, inferences):
		if inferences is not None:
			for inference in inferences:
				inference["variable"].domain.append(inference["removed_value"])
		# TODO consider the conflcit set (inference has "conflict_source" key)

	def backtracking_search(self):
		if self.is_complete():
			return [True]

		variable = self.select_unassigned_variable()
		for value in self.order_domain_values(variable):
			if self.is_consistent(variable, value):
				variable.set_value(value)
				inferences = self.make_inferences(variable)
				if inferences is not None:
					result = self.backtracking_search()
					if result[0]:
						return result
					# TODO consider the conflict set (keep backing up if variable not present)
					# elif variable not in result[1]:
					# 	return result
				variable.clear_value()
				self.remove_inferences(inferences)

		return [False, variable.conflict_set]

	def is_consistent(self, variable, value):
		for constraint in variable.constraints:
			value_map = {variable: value}
			for other_variable in constraint.variables:
				if other_variable.assigned:
					value_map[other_variable] = other_variable.value
			if not constraint.is_satisfied(value_map):
				return False
		return True

	def select_unassigned_variable(self):
		# Makes a list from variables, sorts by degree, then sorts by minimum remaining values
		return sorted(
			# Sorted list decreasing by number of undetermined constraints
			sorted((v for v in self.variables if not v.assigned), key=(lambda var:
				# Counts constraints with not all values assigned
				sum(1 for constraint in var.constraints
					if not all(v.assigned or v == var for v in constraint.variables))),
				reverse=True)
			, key=(lambda var: len(var.domain)))[0]

	def order_domain_values(self, variable):
		binary_constraints = [constraint for constraint in variable.constraints if len(constraint.variables) == 2]
		return sorted(variable.domain, key=(lambda val: self.determine_constrained_values(val, variable, binary_constraints)))

	def determine_constrained_values(self, value, variable, binary_constraints):
		conflicts = 0
		for constraint in binary_constraints:
			other_variable = constraint.variables[0] if constraint.variables[1] == variable else constraint.variables[1]
			for other_value in other_variable.domain:
				if not constraint.is_satisfied({variable: value, other_variable: other_value}):
					conflicts += 1
		return conflicts

	def make_inferences(self, variable=None):
		inferences = []

		queue = deque([])
		if variable is None:
			for arc in self.binary_constraints:
				queue.append((arc.variables[0], arc))
		else:
			for arc in variable.constraints:
				if len(arc.variables) == 2:
					queue.append((variable, arc))

		while queue:
			start, arc = queue.popleft()
			new_inferences = self.remove_inconsistent_values(arc, start)
			if new_inferences is None:
				self.remove_inferences(inferences)
				return None
			elif new_inferences:
				inferences += new_inferences
				next = list(arc.variables)
				next.remove(start)
				for new_arc in next[0].constraints:
					if len(new_arc.variables) == 2:
						queue.append((next[0], new_arc))

		return inferences

	def remove_inconsistent_values(self, constraint, start):
		inferences = []
		other = list(constraint.variables)
		other.remove(start)
		other = other[0]
		if not other.assigned:
			for value2 in list(other.domain):
				relevant = False
				for value1 in start.domain if not start.assigned else [start.value]:
					val_map = { start: value1, other: value2 }
					if constraint.is_satisfied(val_map):
						relevant = True
				if not relevant:
					inferences.append({"variable": other, "removed_value": value2, "conflict_source": start})
					other.domain.remove(value2)
					other.add_conflict(start)
					if not other.domain:
						self.remove_inferences(inferences)
						return None
		return inferences

