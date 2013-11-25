from ConstraintSolver import Variable, Constraint, ConstraintSatisfactionProblem

def austrailia_test():
	domain = ["Red", "Green", "Blue"]
	
	variables = [
		Variable("WA", set(domain)),
		Variable("NT", set(domain)),
		Variable("SA", set(domain)),
		Variable("Q", set(domain)),
		Variable("NSW", set(domain)),
		Variable("V", set(domain)),
		Variable("T", set(domain))
	]

	constraints = [
		Constraint([variables[0], variables[1]], test_not_equal),
		Constraint([variables[0], variables[2]], test_not_equal),
		Constraint([variables[1], variables[2]], test_not_equal),
		Constraint([variables[1], variables[3]], test_not_equal),
		Constraint([variables[2], variables[3]], test_not_equal),
		Constraint([variables[2], variables[4]], test_not_equal),
		Constraint([variables[2], variables[5]], test_not_equal),
		Constraint([variables[3], variables[4]], test_not_equal),
		Constraint([variables[4], variables[5]], test_not_equal)
	]

	problem = ConstraintSatisfactionProblem(variables, constraints)
	return problem.solve()


def test_not_equal(variables, value_map, extras):
	values = set([])
	for variable in value_map:
		if value_map[variable] in values:
			return False
		else:
			values.add(value_map[variable])
	return True

print austrailia_test()

"==================================================================================================="

def schedule_test():
	variables = [
		Variable("Event1", set([("6:00", 90), ("6:25", 90)])),
		Variable("Event2", set([("5:30", 60), ("11:00", 30)])),
		Variable("Event3", set([("5:10", 15), ("1:00", 30)])),
		Variable("Event4", set([("7:00", 60), ("4:30", 30)]))
	]

	constraints = [
		Constraint([variables[2], variables[3]], test_in_order, order=[variables[2], variables[3]]),
		# Constraint([variables[0], variables[1]], test_no_overlap),
		# Constraint([variables[0], variables[2]], test_no_overlap),
		# Constraint([variables[0], variables[3]], test_no_overlap),
		# Constraint([variables[1], variables[2]], test_no_overlap),
		# Constraint([variables[1], variables[3]], test_no_overlap),
		# Constraint([variables[2], variables[3]], test_no_overlap)
		Constraint(variables, test_no_overlap)
	]

	problem = ConstraintSatisfactionProblem(variables, constraints)
	return problem.solve()


def test_no_overlap(variables, value_map, extras):
	values = []
	for key in value_map:
		values.append(value_map[key])

	for i in xrange(len(values)):
		for j in xrange(i):
			time1 = values[i][0]
			length1 = values[i][1]
			time2 = values[j][0]
			length2 = values[j][1]

			if in_order(time1, time2):
				if not in_order(add_time(time1, length1), time2):
					return False
			else:
				if not in_order(add_time(time2, length2), time1):
					return False
	return True


def test_in_order(variables, value_map, extras):
	order = extras["order"]
	for i in xrange(len(order) - 1):
		var1 = order[i]
		var2 = order[i+1]
		if var1 in value_map and var2 in value_map and not in_order(value_map[var1][0], value_map[var2][0]):
			return False
	return True


def split_time(time):
	hours, mins = time.split(":")
	hours = int(hours)
	mins = int(mins)
	return (hours, mins)


def make_time(hours, mins):
	return str(hours) + ":" + str(mins)


def add_time(time, length):
	hours, mins = split_time(time)
	mins += length
	hours += mins / 60
	mins = mins % 60
	hours = hours % 24
	return make_time(hours, mins)


def in_order(time1, time2):
	hours1, mins1 = split_time(time1)
	hours2, mins2 = split_time(time2)
	if hours1 < hours2:
		return True
	if hours1 > hours2 or mins1 > mins2:
		return False
	return True


print schedule_test()