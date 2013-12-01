# TODO throw exceptions if wrong number of variables (in Schedulingconstraints.py)
# TODO throw exception if course required but not in courses requested?

from ConstraintSolver import *
from SchedulingConstraints import *
import urllib2
import json

"""
Creates and returns a schedule with the specified parameters or None if no schedule exists.

Arguments:
	classes_considered (List<string>) names of classes that can be put into this schedule
	parameters (dict<string, ?>) mapping of constraint types to values for those constraints
		Options - max_hours, min_hours, day_start, day_end, classes_needed
	class_variables (List<Variable>) override for getting classes from web, testing purposes

Option Details:
	max_hours, min_hours (int) number of hours, inclusive
	day_start, day_end (string) should be in the format '2000-01-01T%H:%M:%SZ') to match course info
	classes_needed (List<string>) each class should be in the format '[school] [number]', ex. 'CS 1332'
"""
def create_schedule(classes_considered, parameters, class_variables = None):
	variables = []
	if class_variables is None:
		# Define variables through web
		for class_name in (name.split(' ') for name in classes_considered):
			print 'Getting class data for %s %s' % (class_name[0], class_name[1])
			class_info = json.load(urllib2.urlopen('http://course.us.to/school/%s/%s.json' % (class_name[0], class_name[1])))
			# Doesn't store school properly in json, fix
			class_info['school'] = class_name[0]
			sections = []
			for section_name in (section['name'] for section in class_info['sections']):
				sections.append(json.load(urllib2.urlopen('http://course.us.to/school/%s/%s/%s.json' % (class_name[0], class_name[1], section_name))))
			sections.append(None)
			variables.append(Variable(class_info, sections))
	else:
		# Use for testing
		variables = class_variables

	print 'Creating constraint list'
	constraints = []
	for ptype in parameters:
		if ptype == 'max_hours':
			constraints.append(Constraint(variables, max_hours_constraint, max_hours=parameters[ptype]))
		if ptype == 'min_hours':
			constraints.append(Constraint(variables, min_hours_constraint, min_hours=parameters[ptype]))
		if ptype == 'day_start':
			for constraint in create_day_start_constraints(parameters[ptype], variables):
				constraints.append(constraint)
		if ptype == 'day_end':
			for constraint in create_day_end_constraints(parameters[ptype], variables):
				constraints.append(constraint)
		if ptype == 'classes_needed':
			for constraint in create_class_needed_constraints(variables, parameters[ptype]):
				constraints.append(constraint)
	for constraint in create_no_overlap_constraints(variables):
		constraints.append(constraint)

	print 'Solving constraint satisfaction problem'
	problem = ConstraintSatisfactionProblem(variables, constraints)
	return problem.solve()

def create_class_needed_constraints(variables, classes_needed):
	constraints = []
	for class_name in classes_needed:
		for variable in (var for var in variables if str(var.data['school']) + ' ' + str(var.data['name']) == class_name):
			constraints.append(Constraint([variable], needed_class_constraint))
	return constraints