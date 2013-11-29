# TODO data collection
# TODO throw exceptions if wrong number of variables (in Schedulingconstraints.py)
# TODO throw exception if course required but not in courses requested?
# TODO change class name creation in create_class_needed_constraints to match actual attributes
# TODO actually get classes and sections through web
# TODO determine if class names are really the best representation for classes_considered

from ConstraintSolver import *
from SchedulingConstraints import *

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
		for class_name in classes_considered:
			sections = []
			variables.append(Variable(class_name, sections))
	else:
		variables = class_variables

	constraints = []
	for ptype in paramaters:
		if ptype == "max_hours":
			constraints.append(Constraint(variables, max_hours_constraint, "max_hours"=parameters[ptype]))
		if ptype == "min_hours":
			constraints.append(Constraint(variables, min_hours_constraint, "min_hours"=parameters[ptype]))
		if ptype == "day_start":
			for constraint in create_day_start_constraints(parameters[ptype], variables):
				constraints.append(constraint)
		if ptype == "day_end":
			for constraint in create_day_end_constraints(parameters[ptype], variables):
				constraints.append(constraint)
		if ptype == "classes_needed":
			for constraint in create_class_needed_constraints(variables, parameters[ptype):
				constraints.append(constraint)
	for constraint in create_no_overlap_constraints(variables):
		constraints.append(constraint)

	problem = ConstraintSatisfactionProblem(variables, constraints)
	return problem.solve()

def create_class_needed_constraints(variables, classes_needed):
	constraints = []
	for class_name in classes_needed:
		for variable in (var for var in variables if str(var.school) + " " + str(var.number) == class_name):
			constraints.append(Constraint(variable, needed_class_constraint))
	return constraints