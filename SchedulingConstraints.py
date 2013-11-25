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

Variables: 0...n
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
Limits the minimum number of hours taken.

Variables: 0...n
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
Sets an earliest time for classes in the morning.

Variables: 0...n
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
Sets a latest time for classes in the evening.

Variables: 0...n
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

Variables: 0...n
Extras:
	req_class
"""
def needed_class_constraint(variables, value_map, extras):
	if len(variables) > len(value_map):
		return True

	req_class = extras[req_class]
	for variable in (var for var in value_map if value_map[var] is not None):
		if variable == req_class:
			return True
	return False


# TODO data incomplete
"""
Specifies a professor that should not be taken.

Variables: 0...n
Extras:
	bad_professor
"""
def professor_constraint(variables, value_map, extras):
	bad_professor = extras[bad_professor]
	for variable in (var for var in value_map if value_map[var] is not None):
		if variable.professor == bad_professor:
			return False
	return True

