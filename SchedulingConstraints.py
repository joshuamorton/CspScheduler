# Currently assuming that deciding not to take a class is equivalent to a value of None
# Also assuming variables are classes and values are sections

# Attributes of class: professor, credits
# Attributes of section: meetings
# Attributes of meetings: start_time, end_time, monday...

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

from ConstraintSolver import Constraint
import time

"""
Creates binary constraints for ensuring classes do not overlap.
This should be used for any scheduler.
"""
def create_no_overlap_constraints(variables):
	constraints = []
	for var1 in variables:
		for var2 in (var for var in variables if var != var1):
			constraints.append(Constraint([var1, var2], no_overlap_constraint))
	return constraints

"""
Tests if two sections overlap.

Variables: 2
Extras:
	None
"""
def no_overlap_constraint(variables, value_map, extras):
	if variables[0] not in value_map or variables[1] not in value_map:
		return True

	section1 = value_map[variables[0]]
	section2 = value_map[variables[1]]

	if section1 is None or section2 is None:
		return True
	
	for meeting1 in section1['meetings']:
		for meeting2 in section2['meetings']:
			day_overlap = False
			for day in (day for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'] if meeting1[day] and meeting2[day]):
				day_overlap = True
			if day_overlap:
				start1 = time.strptime(meeting1['start_time'], '2000-01-01T%H:%M:%SZ')
				start2 = time.strptime(meeting2['start_time'], '2000-01-01T%H:%M:%SZ')
				end1 = time.strptime(meeting1['end_time'], '2000-01-01T%H:%M:%SZ')
				end2 = time.strptime(meeting2['end_time'], '2000-01-01T%H:%M:%SZ')

				if (start1 > start2 and start1 < end2) or (start2 > start1 and start2 < end1) or (start1 == start2) or (end1 == end2):
					return False
	return True


"""
Limits the maximum number of hours taken.

Variables: 1...n
Extras:
	max_hours
"""
def max_hours_constraint(variables, value_map, extras):
	max_hours = extras['max_hours']
	hours = 0
	for variable in (var for var in value_map if value_map[var] is not None):
		hours += float(variable.data['credits'])
		if hours > max_hours:
			return False
	return True


"""
Limits the minimum number of hours taken.

Variables: 1...n
Extras:
	min_hours
"""
def min_hours_constraint(variables, value_map, extras):
	if len(variables) > len(value_map):
		return True

	min_hours = extras['min_hours']
	hours = 0
	for variable in (var for var in value_map if value_map[var] is not None):
		hours += float(variable.data['credits'])
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
	day_start = time.strptime(extras['day_start'], '2000-01-01T%H:%M:%SZ')
	for variable in (var for var in value_map if value_map[var] is not None):
		for meeting in value_map[variable]['meetings']:
			if time.strptime(meeting['start_time'], '2000-01-01T%H:%M:%SZ') < day_start:
				return False
	return True


"""
Creates unary constraints for setting a latest class time. Preferrable to use this instead of creating constraints.
"""
def create_day_end_constraints(end_time, variables):
	return [Constraint([variable], day_end_constraint, day_end=end_time) for variable in variables]

"""
Sets a latest time for classes in the evening.

Variables: 1...n
Extras:
	day_end
"""
def day_end_constraint(variables, value_map, extras):
	day_end = time.strptime(extras['day_end'], '2000-01-01T%H:%M:%SZ')
	for variable in (var for var in value_map if value_map[var] is not None):
		for meeting in value_map[variable]['meetings']:
			if time.strptime(meeting['end_time'], '2000-01-01T%H:%M:%SZ') > day_end:
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
	bad_professor = extras['bad_professor']
	for variable in (var for var in value_map if value_map[var] is not None):
		if variable['professor'] == bad_professor:
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
Specifies that another class must be taken.

Variables: 1
Extras:
	classes_taken
	prereq
"""
def class_prereq_constraint(variables, value_map, extras):
	if value_map[variables[0]] is None:
		return True

	classes_taken = extras['classes_taken']
	prereq = extras['prereq']
	if prereq in classes_taken:
		return True
	return False