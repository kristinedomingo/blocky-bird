import random
import blocky_bird

random.seed(0)

class dna:
	problem_size = 3
	def __init__(self):
		self.x=[]
		for k in range(0,dna.problem_size):
			self.x.append(random.uniform(-3.0,3.0)) 
	def copy(self):
		new_indiv=dna()
		new_indiv.x=self.x[:]
		return new_indiv

	def mutate(self):
		new_indiv = self.copy()
		to_mutate=random.randint(0,dna.problem_size-1)
		new_indiv.x[to_mutate]+=random.uniform(-1,1)
		return new_indiv

	def crossover(self,other):
		new_indiv = dna()
		for k in range(0,dna.problem_size):
			if random.random()>0.5:
				new_indiv.x[k]=self.x[k]
			else:
				new_indiv.x[k]=other.x[k]
		return new_indiv

	def create_neuron(self):
		new_neuron = neuron()
		new_neuron.weights=self.x
		return new_neuron

	def evaluate(self):
		new_neuron=self.create_neuron()
		self.fitness=evaluate_ann(new_neuron)


class neuron:
	def __init__(self):
		self.weights=[random.uniform(-1.0,1.0),
					  random.uniform(-1.0,1.0),
					  random.uniform(-1.0,1.0)]

	def run(self,inputs):
		total_signal=0.0
		for k in [0,1,2]:
			total_signal+=self.weights[k]*inputs[k]
		if total_signal>0.0:
			return 1.0
		else:
			return -1.0


def evaluate_ann(ann):
	score=blocky_bird.game_function(ann, False)
	return score

