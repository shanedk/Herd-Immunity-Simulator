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

population = 1000
Rnull = 5 # The amount of people an infected person can infect
natImmunity = .1
vacImmunity = .9
vaccinated = .9
pop = []
infected = []

# End user-set values

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
