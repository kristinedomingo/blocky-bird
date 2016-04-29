import random
import blocky_bird

random.seed(0)
problem_size = 3

class individual:
	global problem_size

	def __init__(self):
		self.gene = []
		for k in range(0, problem_size):
			self.gene.append(random.uniform(-problem_size, problem_size))

	def copy(self):
		new_indiv = individual()
		new_indiv.gene = list(self.gene)
		return new_indiv

	def mutate(self):
		new_indiv = self.copy()
		to_mutate = random.randint(0, problem_size - 1)
		new_indiv.gene[to_mutate] += random.uniform(-1, 1)
		return new_indiv

	def crossover(self,other):
		new_indiv = individual()
		for k in range(0, problem_size):
			if random.random()>0.5:
				new_indiv.gene[k]=self.gene[k]
			else:
				new_indiv.gene[k]=other.gene[k]
		return new_indiv

	def create_neuron(self):
		new_neuron = neuron()
		new_neuron.weights=self.gene
		return new_neuron

	def evaluate(self):
		new_neuron=self.create_neuron()
		self.fitness=evaluate_ann(new_neuron)


class neuron:
	global problem_size

	def __init__(self):
		self.weights=[random.uniform(-1.0, 1.0) for i in range(problem_size)]

	def run(self, inputs):
		total_signal = 0.0
		for k in range(problem_size):
			total_signal += self.weights[k] * inputs[k]

		if total_signal > 0.0:
			return 1.0
		else:
			return -1.0


def evaluate_ann(ann):
	score = blocky_bird.game_function(ann, False)
	return score

