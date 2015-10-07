
"""
##########################################################
### @Author Joe Krall      ###############################
### @copyright see below   ###############################

    This file is part of JMOO,
    Copyright Joe Krall, 2014.

    JMOO is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    JMOO is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with JMOO.  If not, see <http://www.gnu.org/licenses/>.
    
###                        ###############################
##########################################################
"""

"Brief notes"
"Algorithms for evolution"

from Algorithms.deap import base
from Algorithms.deap import creator
from Algorithms.deap import tools

import os, sys, inspect

def do_nothing_initializer(problem, population):
    return population, 0


from Algorithms.GALE.gale_components import *
from Algorithms.DE.de_components import *
from Algorithms.MOEA_D.moead_components import *
from Algorithms.NSGAIII.nsgaiii_components import *
from Algorithms.STORM.storm_components import *

    
from jmoo_individual import *



from jmoo_properties import *
from utility import *
import jmoo_stats_box
import array,random,numpy


#############################################################
### MOO Algorithms
#############################################################

class jmoo_NSGAII:
    def __init__(self, color="Blue"):
        self.name = "NSGAII"
        self.initializer = None
        self.selector = selTournamentDCD
        self.adjustor = crossoverAndMutation
        self.recombiner = selNSGA2
        self.color = color
        self.type = '^'
    
class jmoo_SPEA2:
    def __init__(self, color="Green"):
        self.name = "SPEA2"
        self.initializer = None
        self.selector = selTournament
        self.adjustor = crossoverAndMutation
        self.recombiner = selSPEA2
        self.color = color
        self.type = 'h'
        
class jmoo_GALE:
    def __init__(self, color="Red"):
        self.name = "GALE"
        self.initializer = None
        self.selector = galeWHERE
        self.adjustor = galeMutate
        self.recombiner = galeRegen
        self.color = color
        self.type = '*'

class jmoo_DE:
    def __init__(self, color="Black"):
        self.name = "DE"
        self.initializer = None
        self.selector = de_selector
        self.adjustor = de_mutate
        self.recombiner = de_recombine #stub
        self.color = color
        self.type = 'o'

class jmoo_MOEAD:
    def __init__(self, color="Blue"):
        self.name = "MOEAD"
        self.initializer = initialize_population
        self.selector = moead_selector
        self.adjustor = moead_mutate
        self.recombiner = moead_recombine
        self.color = color
        self.type = '*'

class jmoo_NSGAIII:
    def __init__(self, color="blue"):
        self.name = "NSGA3"
        self.initializer = None
        self.selector = nsgaiii_selector
        self.adjustor = nsgaiii_sbx
        self.recombiner = nsgaiii_recombine
        self.color = color
        self.type = 'p'

class jmoo_ANYWHERE:
    def __init__(self, color="Yellow"):
        self.name = "ANYWHERE"
        self.initializer = None
        self.selector = anywhere_selector
        self.adjustor = anywhere_mutate
        self.recombiner = anywhere_recombine
        self.color = color
        self.type = '*'

class jmoo_ANYWHERE2:
    def __init__(self, color="Green"):
        self.name = "ANYWHERE2"
        self.initializer = None
        self.selector = anywhere3_selector
        self.adjustor = anywhere_mutate
        self.recombiner = anywhere_recombine
        self.color = color
        self.type = 'p'


class Bin:
    def __init__(self):
        self.low=0
        self.up=0
        self.mid=0
        
def binner(problem, mu):    
    numBins = 10
    Bins = [Bin() for x in problem.decisions]
    for dec in problem.decisions:
        for bin in range(numBins):
            Bins[bin].low = dec.low + (bin  )*((dec.up - dec.low)/numBins)
            Bins[bin].up  = dec.low + (bin+1)*((dec.up - dec.low)/numBins)
            Bins[bin].mid = (Bins[bin].up - Bins[bin].low) / 2
    
    #random initial sample - pick bins for each decision
    initialBins = []
    for dec in problem.decisions:
        initialBins.append(random.randint(0, numBins-1))
    population = []
    population.append(initialBins)
    
    #build population sample
    for i in range(mu-1):
        furthest = 0
        
        #glob
        
        
    
#############################################################
### MOO Algorithm Selectors
#############################################################
 
    
    
def selTournament(problem, individuals):
    
    # Format a population Data structure usable by DEAP's package
    dIndividuals = deap_format(problem, individuals)
    
    # Select elites
    selectees = tools.selTournament(dIndividuals, len(individuals), 4)
    
    # Update beginning population Data structure
    selectedIndices = [i for i,sel in enumerate(selectees)]
    return [individuals[s] for s in selectedIndices], len(individuals)

def selTournamentDCD(problem, individuals):
    
    # Evaluate any new guys
    for individual in individuals:
        if not individual.valid:
            individual.evaluate()
            
    # Format a population Data structure usable by DEAP's package
    dIndividuals = deap_format(problem, individuals)
    
    # Assign crowding distance
    tools.emo.assignCrowdingDist(dIndividuals)
    
    # Select elites
    selectees = tools.selTournamentDCD(dIndividuals, len(individuals))
    
    # Update beginning population Data structure
    selectedIndices = [i for i,sel in enumerate(selectees)]
    return [individuals[s] for s in selectedIndices], len(individuals)

#############################################################
### MOO Algorithm Adjustors
#############################################################

def helper_list(lst, item):

    item = [int(item[0]), int(item[1]), round(item[2], 2), int(item[3]), round(item[4], 2)]
    # print " >>>>", item, len(lst)
    if len(lst) == 0 or item not in lst:
        lst.append(item)
        return lst
    else:
        return lst

def crossoverAndMutation(problem, individuals):

    from copy import copy
    new_individuals = individuals

    # Format a population Data structure usable by DEAP's package
    dIndividuals = deap_format(problem, individuals)
    new_dIndividuals = []
    # print "Number of Individuals: ", len(dIndividuals)

    # Crossover
    for ind1, ind2 in zip(dIndividuals[::2], dIndividuals[1::2]):
        if random.random() <= 1: #crossover rate
            # print ".",
            ind1, ind2 = tools.cxUniform(ind1, ind2, indpb=1.0/len(problem.decisions))
            new_dIndividuals.append(ind1)
            new_dIndividuals.append(ind2)
        else:
            new_dIndividuals.append(ind1)
            new_dIndividuals.append(ind2)



    # Mutation
    for ind in new_dIndividuals:
        # print "+",
        tools.mutPolynomialBounded(ind, eta = 1.0, low=[dec.low for dec in problem.decisions], up=[dec.up for dec in problem.decisions], indpb=0.1 )
        del ind.fitness.values

    # Update beginning population Data structure
    for individual, dIndividual in zip(new_individuals, new_dIndividuals):
        for i in range(len(individual.decisionValues)):
            individual.decisionValues[i] = dIndividual[i]
            individual.fitness = None


    return new_individuals,0

def variator(problem, selectees):
    return selectees, 0
    " jiggle everyone by ~ 1% "
    # Variation
    d = 0.0 #0.03
    for r_index,row in enumerate(selectees):
        for i in range(len(problem.decisions)):
            selectees[r_index].decisionValues[i] = max(problem.decisions[i].low, min(problem.decisions[i].up,  row.decisionValues[i] + (random.uniform(0.0, d)-d/2) * (problem.decisions[i].up  - problem.decisions[i].low)))
    
    
    return selectees, 0

#############################################################
### MOO Algorithm Recombiners
#############################################################


def selSPEA2(problem, population, selectees, k):
    # Evaluate any new guys
    for individual in population+selectees:
        if not individual.valid:
            individual.evaluate()
            
    # Format a population Data structure usable by DEAP's package
    dIndividuals = deap_format(problem, population+selectees)
    
    # Combine
    dIndividuals = tools.selSPEA2(dIndividuals, k)
    
    # Copy from DEAP structure to JMOO structure
    population = []
    for i,dIndividual in enumerate(dIndividuals):
        cells = []
        for j in range(len(dIndividual)):
            cells.append(dIndividual[j])
        population.append(jmoo_individual(problem, cells, dIndividual.fitness.values))
        
        
    return population,k

def selNSGA2(problem, population, selectees, k):
    
    # Evaluate any new guys
    for individual in population+selectees:
        if not individual.valid:
            individual.evaluate()
            
    # Format a population Data structure usable by DEAP's package
    dIndividuals = deap_format(problem, population+selectees)
    
    # Combine
    dIndividuals = tools.selNSGA2(dIndividuals, k)
    
    # Copy from DEAP structure to JMOO structure
    population = []
    for i,dIndividual in enumerate(dIndividuals):
        cells = []
        for j in range(len(dIndividual)):
            cells.append(dIndividual[j])
        population.append(jmoo_individual(problem, cells, dIndividual.fitness.values))
        
    return population,k

#############################################################
### MOO Algorithm Convergence Stops
#############################################################

def default_toStop(statBox):
    return False

def bstop(statBox):
    stop = True
    for o,obj in enumerate(statBox.problem.objectives):
        if statBox.box[-1].changes[o] <= statBox.bests[o]: stop = False
    
    if stop == True:
        statBox.lives += -1
        print "#"*20
        
    return stop and statBox.lives == 0


#############################################################
### MOO Algorithm Utility
#############################################################

def deap_format(problem, individuals):
    "copy a jmoo-style list of individuals into a deap-style list of individuals"
    toolbox = base.Toolbox()
    creator.create("FitnessMin", base.Fitness, weights=[-1.0 if obj.lismore else 1.0 for obj in problem.objectives])
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

    dIndividuals = []
    for i,individual in enumerate(individuals):
        dIndividuals.append(creator.Individual([dv for dv in individual.decisionValues]))
        dIndividuals[-1].fitness.decisionValues = [dv for dv in individual.decisionValues]
        if individual.valid: dIndividuals[i].fitness.values = individual.fitness.fitness
        dIndividuals[-1].fitness.feasible = not problem.evalConstraints([dv for dv in individual.decisionValues])
        dIndividuals[-1].fitness.problem = problem
        
    
    return dIndividuals 
       