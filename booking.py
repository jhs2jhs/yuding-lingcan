
from datetime import datetime

day_last = 7
hour_min = 8
hour_max = 18
status_booked = 1
status_free = 0

class Room:
	def __init__(self, rid):
		self.rid = rid
		self.booked = {}
		self.init_booked()

	def init_booked(self):
		for day in range(0, day_last):
			if not self.booked.has_key(day):
				self.booked[day] = {}
			for hour in range(hour_min, hour_max):
				if not self.booked[day].has_key(hour):
					self.booked[day][hour] = {}
				self.booked[day][hour]['booking'] = status_free ## 0 == not booked, 1 == booked
				self.booked[day][hour]['booker'] = ''
				#print day, hour

	def is_booked(self, day, hour):
		return self.booked[day][hour]['booking'] == status_free

	def get_available_time_on_specific_day(self, day):
		booked = self.booked[day]
		return booked

	def show_booking_on_specific_day(self, day):
		booked = self.get_available_time_on_specific_day(day)
		t_hour = u''
		t_booking = u''
		for hour in range(hour_min, hour_max):
			t_hour += str(hour)
			if hour > 12:
				t_hour += 'pm'
			else:
				t_hour += 'am'
			#print booked
			if booked[hour]['booking'] == status_free:
				t_booking += u'\u2713'
			else:
				t_booking += u'\u2718'
			if hour != 17:
				t_hour += '\t|'
				t_booking += '\t|'
		print u"=====================================[day: %s]===================================="%day
		print t_hour
		print t_booking
		#print u"-----------------------------------------------------------------------------------"

	def show_booking_on_today(self, hour_current):
		booked = self.get_available_time_on_specific_day(0)
		t_hour = u''
		t_booking = u''
		for hour in range(hour_min, hour_max):
			if hour_current > hour:
				t_hour += '\t'
				t_booking += '\t'
			else:
				t_hour += str(hour)
				if hour > 12:
					t_hour += 'pm'
				else:
					t_hour += 'am'
				#print booked
				if booked[hour]['booking'] == status_free:
					t_booking += u'\u2713'
				else:
					t_booking += u'\u2718'
				if hour != 17:
					t_hour += '\t|'
					t_booking += '\t|'
		print u"=====================================[today : 0]===================================="
		print t_hour
		print t_booking
		print u"-----------------------------------------------------------------------------------"

	def book(self, day, hour):
		if not day in range(0, day_last):
			return False, "invalidate day"
		if not hour in range(hour_min, hour_max):
			return False, "invalidate hour"
		if self.booked[day][hour]['booking'] == status_free:
			self.booked[day][hour]['booking'] = status_booked
			return True, u"This room booked by you for day %s at hour %s"%(day, hour)
		else:
			return False, u"This room has booked by other for day %s at hour %s"%(day, hour)


class BookingEngine:
	def __init__(self, room):
		self.room = room
		self.hour_current = self.now().hour
		self.hour_current = 14 ## comment it in real case

	def now(self):
		return datetime.now()

	def welcome(self):
		print "== "
		print "== Welcome to room booking system"
		print "== The current time is %s"%(str(self.now()))
		print "== You can use this system to book thr room for next %s days, and each day from %sam to %spm"%(day_last, hour_min, hour_max)
		print "== Please check today's booking:"
		print "== [day 0 = today, day 1 = tomorrow, etc]"
		print u"== [\u2713 = free,  \u2718 = booked]"
		self.room.show_booking_on_today(self.hour_current) 

	def run(self):
		print "=="
		action = raw_input("== Your action? [booking, view]: ")
		self.step(action)

	def step(self, action):
		action = action.lower()
		if not action in ['booking', 'view']:
			print "== Invalidate typing, please try again !!!"
			self.run()
		if action == 'view':
			self.step_view()
			return self.run()
		if action == 'booking':
			print "=="
			day = self.step_booking_day()
			hour = self.step_booking_hour(day)
			status, msg = self.room.book(day, hour)
			if status == True:
				print "==", msg
			else:
				print "==", msg
				print "== please view and select another day or hour"
			return self.run()


	def step_booking_day(self):
		try:
			print range(0, day_last)
			day = raw_input(u"== please select from above day: ")
			day = int(day)
			if not day in range(0, day_last):
				print "== wrong day, please try again"
				return self.step_booking_day()
			else:
				return day
		except Exception as e:
			print "== exception: wrong day, please try again"
			return self.step_booking_day()

	def step_booking_hour(self, day):
		try:
			hour_temp = hour_min
			if day == 0:
				hour_temp = self.hour_current
			print range(hour_temp, hour_max)
			hour = raw_input(u"== please select the hour from above you want to book on day %s ?: "%(day))
			hour = int(hour)
			if not hour in range(hour_temp, hour_max):
				print "== wrong hour, please try again"
				return self.step_booking_hour(day)
			else:
				return hour
		except Exception as e:
			print "== exception: wrong hour, please try again"
			#return self.step_booking_hour(day)

	def step_view(self):
		print "== [day 0 = today, day 1 = tomorrow, etc]"
		print u"== [\u2713 = free,  \u2718 = booked]"
		self.room.show_booking_on_today(self.hour_current) 
		for day in range(1, day_last):
			self.room.show_booking_on_specific_day(day)

def main():
	room = Room(5)
	booking_engine = BookingEngine(room)
	booking_engine.welcome()
	booking_engine.run()


if __name__ == "__main__":
	main()


