inFile = open("input.txt","r")
outFile = open("output.txt","w")
import random

# Part - 01
outFile.write("Part - 01\n")
def createInitialPopulation(N, T, populationSize):
    population = []
    for i in range(populationSize):
        chromosome = ""
        for j in range(N * T):
            chromosome += random.choice(('0','1'))
        population.append(chromosome)
    return population


def fitnessCalculation(N, T, chromosomes):
    fitnessArray = []
    for i in range(len(chromosomes)):
        overlapPenalty, consistency = 0, 0
        courseTracker = [0] * N

        for slot in range(T):
            timeSlot = chromosomes[i][slot * N:(slot + 1) * N]
            count = 0

            for k in range(N):
                if timeSlot[k] == '1':
                    count += 1
                    courseTracker[k] += 1
            if count != 0:
                overlapPenalty += count - 1

        for l in range(len(courseTracker)):
            consistency += abs(courseTracker[l] - 1)
        totalPenalty = overlapPenalty + consistency
        fitnessArray.append(-totalPenalty)
    return fitnessArray


def randomSelection(population):
    selectedPairs = []
    unselectedIndices = list(range(len(population)))
    populationSize = len(population)

    if populationSize <= 1:
        return None

    while len(unselectedIndices) >= 2:
        indexA = random.choice(unselectedIndices)
        unselectedIndices.remove(indexA)
        indexB = random.choice(unselectedIndices)
        unselectedIndices.remove(indexB)
        selectedPairs.append([indexA, indexB])
    return selectedPairs


def singlePointCrossover(population, pairs):
    for pair in pairs:
        parent1, parent2 = pair
        crossoverPoint = random.randint(0, len(population[parent1]) - 1)

        parent1Left = population[parent1][:crossoverPoint]
        parent2Left = population[parent2][:crossoverPoint]
        parent1Right = population[parent1][crossoverPoint:]
        parent2Right = population[parent2][crossoverPoint:]

        child1 = parent1Left + parent2Right
        child2 = parent2Left + parent1Right

        child1 = mutate(child1)
        child2 = mutate(child2)

        population[parent1] = child1
        population[parent2] = child2
    return population


def mutate(string):
    indexA = random.randint(0, len(string) - 1)
    indexB = random.randint(indexA, len(string) - 1)

    segmentSize = indexB - indexA
    mutationSegment = ""
    for i in range(segmentSize):
        mutationSegment += random.choice(('0','1'))

    mutatedString = string[:indexA] + mutationSegment + string[indexB:]
    return mutatedString


# Part - 02
def randomSelectionForTwoPointCrossover(population):
    populationSize = len(population)
    if populationSize == 1:
        return None

    indexA = random.randint(0, populationSize - 1)
    indexB = random.randint(0, populationSize - 1)

    while indexB == indexA:
        indexB = random.randint(0, populationSize - 1)

    return [indexA, indexB]


def twoPointCrossover(population, parent1, parent2):
    crossoverPoint1 = random.randint(0, len(population[parent1]) - 1)
    crossoverPoint2 = random.randint(crossoverPoint1, len(population[parent2]) - 1)

    child1 = population[parent1][:crossoverPoint1] + population[parent2][crossoverPoint1:crossoverPoint2] + population[parent1][crossoverPoint2:]
    child2 = population[parent2][:crossoverPoint1] + population[parent1][crossoverPoint1:crossoverPoint2] + population[parent2][crossoverPoint2:]
    outFile.write(f"After two-point crossover two resultant offsprings are, {child1} & {child2}")


def geneticAlgorithm(maxGenerations, populationSize):
    N, T = list(map(int, inFile.readline().split()))
    population = createInitialPopulation(N, T, populationSize)

    flag = True
    for i in range(maxGenerations):
        fitnessScores = fitnessCalculation(N, T, population)

        if 0 in fitnessScores:
            index = fitnessScores.index(0)
            result = f"{population[index]}\n0\n"
            outFile.write(result)
            flag = False
            break

        selectedParentPairs = randomSelection(population)
        if selectedParentPairs is None:
            outFile.write("Not enough population")
            flag = False
            break

        population = singlePointCrossover(population, selectedParentPairs)

    if flag:
        maxFitnessScore = max(fitnessScores)
        index = fitnessScores.index(maxFitnessScore)
        result = f"{population[index]}\n{maxFitnessScore}"
        outFile.write(result)

    parent1, parent2 = randomSelectionForTwoPointCrossover(population)
    outFile.write("\nPart - 02\n")
    twoPointCrossover(population, parent1, parent2)

maxGenerations, populationSize = 100, 50
geneticAlgorithm(maxGenerations, populationSize)
inFile.close()
outFile.close()