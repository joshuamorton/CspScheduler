# Attributes of class: professor, credits, college, name
# Attributes of section: meetings
# Attributes of meetings: start_time, end_time, monday...

"""
	max_hours, min_hours (int) number of hours, inclusive
	day_start, day_end (string) should be in the format '2000-01-01T%H:%M:%SZ') to match course info
	classes_needed (List<string>) each class should be in the format '[school] [number]', ex. 'CS 1332'
"""

import ConstraintParser
import ConstraintSolver

parameters = {
	'max_hours': 15,
	'min_hours': 9,
	'day_start': '2000-01-01T9:00:00Z',
	'day_end': '2000-01-01T17:00:00Z',
	'classes_needed': ['CS 1332', 'CS 2050', 'CS 4001']
}

classes = ["CS 1332", "CS 2050", "CS 4001", "CHEM 1211K", "MATH 1502"]

solution = ConstraintParser.create_schedule(classes, parameters)

if solution is None:
	print "No schedule possible."
else:
	for clas in solution:
		print clas.data['school'], ' ', clas.data['name']
		section = solution[clas]
		if section is None:
			print 'Not in schedule'
		else:
			for meeting in section['meetings']:
				m = 'M' if meeting['monday'] else ' '
				t = 'T' if meeting['tuesday'] else ' '
				w = 'W' if meeting['wednesday'] else ' '
				r = 'R' if meeting['thursday'] else ' '
				f = 'F' if meeting['friday'] else ' '
				print m, t, w, r, f, " ", meeting['start_time'][11:19], '-', meeting['end_time'][11:19]
		print