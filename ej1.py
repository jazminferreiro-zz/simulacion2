import random
import math


class Exponential_distribution:
	def __init__(self, lamda):
		self.lamda = lamda

	def distribution(self, x):
		return math.exp(-x*self.lamda)

	def generate(self):
		u = random.uniform(0, 1)
		if(u > 1):
			raise ValueError('u must be less than 1.')
		x = -math.log(1-u)/self.lamda
		return x

	def generate_list(self, n):
		l= []
		for i in range(n):
			l.append(self.generate())
		return l

class Request_time:
	def __init__(self, process_duration, wait_duration):
		self.process_duration = process_duration
		self.wait_duration = wait_duration

	def get_prcess_duration(self):
		return self.process_duration

	def get_wait_duration(self):
		return self.wait_duration


class Web_service:


	def attend(self, arrival_times):
		request_times1 = self.twoBases(arrival_times)
		request_times2 = self.oneBase(arrival_times)
		total_wait_duration1 = 0
		total_duration1 = 0
		no_wait1 = 0
		for t in request_times1:
			if(t.get_wait_duration() == 0):
				no_wait1 += 1
			total_wait_duration1 += t.get_wait_duration()
			#tiempo en fila + tiempo de procesamiento
			total_duration1 +=  t.get_wait_duration() + t.get_prcess_duration()

		avarage_wait1 = total_wait_duration1/len(request_times1)
		avarage_duration1 = total_duration1/len(request_times1)
		no_wait1 = ((no_wait1+0.0)/len(request_times1))


		total_wait_duration2 =0
		total_process2 = 0
		total_duration2 = 0
		no_wait2 = 0
		for t in request_times2:
			if(t.get_wait_duration() == 0):
				no_wait2 += 1
			total_wait_duration2 += t.get_wait_duration()
			#tiempo en fila + tiempo de procesamiento
			total_duration2 +=  t.get_wait_duration() + t.get_prcess_duration()


		avarage_wait2 = total_wait_duration2/len(request_times2)
		avarage_duration2 =total_duration2/len(request_times2)
		no_wait2 = ((no_wait2+0.0)/len(request_times2))

		print "\nTiempo medio de espera entre que la solicitud llega y puede ser procesada: "
		print "opvion 1 (dos bases)  = %f \nopcion 2 (una base) = %f"  %(avarage_wait1, avarage_wait2)

		print "\nLa fraccion de las solicitudes que no esperaron para ser procesadas"
		print "opvion 1 (dos bases)  = %f \nopcion 2 (una base) = %f"  %(no_wait1, no_wait2)

		print "\nTiempo medio que demora en resolver cada solicitud (tiempo en fila + tiempo de procesamiento)"
		print "opvion 1 (dos bases)  = %f \nopcion 2 (una base) = %f" %(avarage_duration1,avarage_duration2)

		#la empresa solo acepta realizar la inversion si el tiempo medio que demora en resolver cada solicitud
		#de la opcion 1 es como minimo 50% menor que la opcion 2.
		if(avarage_duration1 <= avarage_duration2*0.5):
			print "Se acepta la inversion porque el 50 por ciento de la opcion 2 es %f" %(avarage_duration2*0.5)


	def twoBases(self, arrive_times):
		base1 = Exponential_distribution(0.7)
		t_base1_free = 0

		base2 = Exponential_distribution(1)
		t_base2_free = 0

		request_times = []

		for i in range(len(arrive_times)):
			t = arrive_times[i]
			u = random.uniform(0,1)
			if(u < 0.6):
				t_process = base1.generate()
				t_base1_free = self.get_request_times(request_times, t, t_process, t_base1_free)
			else:
				t_process = base2.generate()
				t_base2_free = self.get_request_times(request_times, t, t_process, t_base2_free)
		return request_times



	def oneBase(self, arrive_times):
		base = Exponential_distribution(0.8)
		process_times = base.generate_list(len(arrive_times))
		request_times = []
		t_base_free = 0;
		for i in range(len(arrive_times)):
			t = arrive_times[i]
			t_process = process_times[i]
			t_base_free = self.get_request_times(request_times, t, t_process, t_base_free)
		return request_times

	def get_request_times(self, request_times, t, t_process, t_base_free):
		if(t > t_base_free):
			#si el request cae en un instante de tiempo en el cual la base esta libre -> se procesa sin esperar
			t_base_free = t + t_process
			request_times.append(Request_time(t_process, 0))
		else:
			#sino tiene que esperar a que la base se libere
			wait_duration = t_base_free - t
			t_base_free = t_base_free + t_process
			request_times.append(Request_time(t_process,wait_duration ))
		return t_base_free;




if __name__ == '__main__':
	cant = 100000
	exp = Exponential_distribution(4)
	l = exp.generate_list(cant)
	prev = 0
	for i in range(len(l)):
		l[i] = l[i] + prev
		prev = l[i]

	service = Web_service()
	service.attend(l);
