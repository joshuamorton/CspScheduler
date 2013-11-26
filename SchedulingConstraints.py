# Currently assuming that deciding not to take a class is equivalent to a value of None
# Also assuming variables are classes and values are sections

# Unavailable:
# Professors
# List of courses taken (transcript)
# Course prerequisites

"""
Each constraint function must take in applicable variables, a value map, and extras.
Required extras should be specified, as well as the number of variables.
Returns True if satisfied or False otherwise.
Is satisfaction is unclear, return True.
"""


"""
Limits the maximum number of hours taken.

Variables: 1...n
Extras:
	max_hours
"""
def max_hours_constraint(variables, value_map, extras):
	max_hours = extras[max_hours]
	hours = 0
	for variable in (var for var in value_map if value_map[var] is not None):
		hours += variable.credits
		if hours > max_hours:
			return False
	return True


"""
Creates unary constraints for min hours. Preferrable to use this instead of creating constraints.
"""
def create_min_hours_constraints(min_hours, variables):
	return [Constraint([variable], min_hours_constraint, min_hours) for variable in variables]

"""
Limits the minimum number of hours taken.

Variables: 1...n
Extras:
	min_hours
"""
def min_hours_constraint(variables, value_map, extras):
	if len(variables) > len(value_map):
		return True

	min_hours = extras[min_hours]
	hours = 0
	for variable in (var for var in value_map if value_map[var] is not None):
		hours += variable.credits
		if hours > min_hours:
			return True
	return False


"""
Creates unary constraints for setting an earliest class time. Preferrable to use this instead of creating constraints.
"""
def create_day_start_constraints(start_time, variables):
	return [Constraint([variable], day_start_constraint, day_start=start_time) for variable in variables]

"""
Sets an earliest time for classes in the morning.

Variables: 1...n
Extras:
	day_start
"""
def day_start_constraint(variables, value_map, extras):
	day_start = extras[day_start]
	for variable in (var for var in value_map if value_map[var] is not None):
		for meeting in value_map.meetings:
			if meeting.start_time < day_start:
				return False
	return True


"""
Creates unary constraints for setting a latest class time. Preferrable to use this instead of creating constraints.
"""
def create_day_end_constraints(end_time, variables):
	return [Constraint([variable], day_start_constraint, day_end=end_time) for variable in variables]

"""
Sets a latest time for classes in the evening.

Variables: 1...n
Extras:
	day_end
"""
def day_end_constraint(variables, value_map, extras):
	day_end = extras[day_end]
	for variable in (var for var in value_map if value_map[var] is not None):
		for meeting in value_map.meetings:
			if meeting.end_time > day_end:
				return False
	return True


"""
Requires a class to be taken.

Variables: 1
Extras:
	None
"""
def needed_class_constraint(variables, value_map, extras):
	if value_map[variables[0]] is None:
		return False
	return True


# TODO data incomplete
"""
Specifies a professor that should not be taken.

Variables: 1...n
Extras:
	bad_professor
"""
def professor_constraint(variables, value_map, extras):
	bad_professor = extras[bad_professor]
	for variable in (var for var in value_map if value_map[var] is not None):
		if variable.professor == bad_professor:
			return False
	return True


"""
Creates prereq constraints for each variable that has a prerequisite. Requirements should be expressed
in prereqs as a dictionary from the course to its prerequisite.
"""
def create_class_prereq_constraints(variables, prereqs, classes):
	return [Constraint([variable], class_prereq_constraint, classes_taken=classes, prereq=prereqs[variable])
			for variable in (var for var in variables if var in prereqs)]

"""
Specifies that another class must be in 

Variables: 1
Extras:
	classes_taken
	prereq
"""
def class_prereq_constraint(variables, value_map, extras):
	if value_map[variables[0]] is None:
		return True

	classes_taken = extras[classes_taken]
	prereq = extras[prereq]
	if prereq in classes_taken:
		return True
		return False