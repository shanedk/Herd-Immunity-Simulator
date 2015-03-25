#!/usr/bin/env python3
#    Herd Immunity Simulator
#    Copyright 2015 Shane D. Killian
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# User can set these values:
def restricted_vaccination(float_input):
    x = float(float_input)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not within range (0.0, 1.0)"%(x,))
    if x == 0.0 or x == 1.0:
        raise argparse.ArgumentTypeError("0 or 1 are not acceptable inputs for vaccination rate")
    return x
def restricted_immunity(float_input):
    x = float(float_input)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range (0.0, 1.0)"%(x,))
    return x
def restricted_population(int_input):
    x=int(int_input)
    if x <= 0:
        raise argparse.ArgumentTypeError("Population must be greater than 0")
    return x
def restricted_Rnull(int_input):
    x=int(int_input)
    if x <= 0:
        raise argparse.ArgumentTypeError("Rnull must be greater than 0")
    return x
import argparse

parser = argparse.ArgumentParser(description='simulate spread of infection in a population')

parser.add_argument('-p', '--population', type=restricted_population, dest='population', default=[1000], nargs=1,
                    help='set the size of the population')
parser.add_argument('-r','--Rnull', type=restricted_Rnull, dest='Rnull', default=[5], nargs=1,
                    help='The amount of people an infected person can infect')
parser.add_argument('-n','--natImmunity', type=restricted_immunity, dest='natImmunity', default=[0.1], nargs=1,
                    help='natural immunity of the population to the disease' +
                         '(chance of an exposed unvaccinated person of resisting infection)')
parser.add_argument('-v','--vacImmunity', type=restricted_immunity, dest='vacImmunity', default=[0.9], nargs=1,
                    help='immunity conferred by vaccination (chance to resist infection)')
parser.add_argument('-V','--vaccRate', type=restricted_vaccination, dest='vaccinated', default=[0.9], nargs=1,
                    help='percentage of the population that has been vaccinated')
parser.add_argument('--debug', dest='debug_flag', default=False, action='store_true',
                    help='print additional debug output')
args = parser.parse_args()

population = args.population[0]
Rnull = args.Rnull[0]
natImmunity = args.natImmunity[0]
vacImmunity = args.vacImmunity[0]
vaccinated = args.vaccinated[0]

if args.debug_flag:
    print("\n\npopulation value: %d" % population)
    print("Rnull value: %d" % Rnull)
    print("natImmunity value: %f" % natImmunity)
    print("vacImmunity value: %f" % vacImmunity)
    print("vaccinated value: %f\n\n" % vaccinated)

#if
# End user-set values

pop = []
infected = []

import random,sys

sys.setrecursionlimit(population*Rnull) # We're going to be doing a LOT of recursion!

def initPop():
    for i in range(population):
        r = random.random()
        pop.append(r<=vaccinated)
        infected.append(False)

def evalPop():
    unVac = 0
    vac = 0
    iVac = 0
    iUnVac = 0
    hVac = 0
    hUnVac = 0
    herd = 1 - (1 / Rnull)

    for i in range(population):
        if pop[i]:
            vac += 1
            if infected[i]:
                iVac += 1
            else:
                hVac += 1
        else:
            unVac += 1
            if infected[i]:
                iUnVac += 1
            else:
                hUnVac += 1
    immune = (vac*vacImmunity + unVac*natImmunity)/population
    isHerd = immune>=herd
    print("Vaccinated: " + str(vac) + " (" + str(round(vac*100/population,1)) + "%)")
    print("Unvaccinated: " + str(unVac) + " (" + str(round(unVac*100/population,1)) + "%)")
    print("Healthy vaccinated: " + str(hVac) + " (" + str(round(hVac*100/vac,1)) + "% of vaccinated)")
    print("Healthy unvaccinated: " + str(hUnVac) + " (" + str(round(hUnVac*100/unVac,1)) + "% of unvaccinated)")
    print("Infected vaccinated: " + str(iVac) + " (" + str(round(iVac*100/vac,1)) + "% of vaccinated)")
    print("Infected unvaccinated: " + str(iUnVac) + " (" + str(round(iUnVac*100/unVac,1)) + "% of unvaccinated)")
    print("Herd Immunity: " + str(isHerd) + " (" + str(round(herd*100,1)) + "% needed for Herd Immunity; we have "+str(round(immune*100,1))+"%)")

def infectNode(node):
    if not(infected[node]): # We don't do anything if it's already infected
        r = random.random()
        if pop[node]:
            infect = (r>vacImmunity)
        else:
            infect = (r>natImmunity)
        if infect:
            infected[node] = True
            infectSpread(node)

def infectSpread(node):
    while True: # Let's make sure our given node isn't in that list
        rNodes = random.sample(range(0,population),Rnull)
        if not(node in rNodes):
            break
    for n in rNodes:
        infectNode(n)

def initInfect():
    node = int(random.random()*population)
    infected[node] = True # The first one is always infected no matter what
    infectSpread(node)

initPop()

initInfect()

evalPop()
