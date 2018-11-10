import random
import simpy
import numpy




class Granja(object):
    def __init__(self, env, count, server_selection):
        self.env = env
        self.count = count
        self.servers = [simpy.Resource(env) for x in range(count)]
        self.server_selection = server_selection
        self.rr = 0

    def attend(self, request):
        server = self.select_server_option2()
        if(self.server_selection == 1 ):
            server = self.select_server_option1()
        with server.request() as req:
            yield req
            yield self.env.timeout(request.get_process_duration())

    def select_server_option1(self):
        queues = []

        for x in self.servers:
            if (x.count == 0) and (len(x.queue) == 0):
                return x
            else:
                queues.append(len(x.queue))

        return self.servers[numpy.array(queues).argmin()]

    def select_server_option2(self):
        self.rr += 1
        if(self.rr >= self.count):
            self.rr = 0
        return self.servers[self.rr]



class Request(object):

    request_duration = {
        'A': (60,180),
        'B': (120,360),
        'C': (200,800)
    }

    def __init__(self, env):
        self.env = env
        self.type = numpy.random.choice(['A', 'B', 'C'], p=[0.7, 0.2, 0.1])

    def attended_by(self, granja):
        yield self.env.process(granja.attend(self))
        print("Request type %s attended at %.2f  " % (self.type,self.env.now))

    def get_process_duration(self):
         a =  self.request_duration[self.type][0]
         b = self.request_duration[self.type][1]
         return random.randint(a,b)



def generate_requests(environment, count, granja):
    for i in range(count):
        request = Request(env)
        environment.process(request.attended_by(granja))
        t = random.expovariate(1.0 / 45)
        yield environment.timeout(t)


#--------------------------------------


env = simpy.Environment()

granja_option1 = Granja(env, 5, 1)
print "seleccion inteligente"
env.process(generate_requests(env,10, granja_option1))
env.run()

print "\nround robin"
granja_option2 = Granja(env, 5, 2)
env.process(generate_requests(env,10, granja_option2))
env.run()
