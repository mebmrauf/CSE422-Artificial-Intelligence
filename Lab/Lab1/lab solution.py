import heapq

# creating the roadmap and heuristic distance graph
def graphHeuristic(infile):
    adjacencyList, heuristics, destination = {}, {}, None

    for citydetails in infile:
        cityInfo = citydetails.split()
        city = cityInfo[0]
        heuristics[city] = int(cityInfo[1])
        if heuristics[city] == 0:
            destination = city
        neighbors = [(cityInfo[i], int(cityInfo[i+1])) for i in range(2, len(cityInfo), 2)]
        adjacencyList[city] = neighbors

    return adjacencyList, heuristics, destination

# apply A* search
def aStarSearch(graph, heuristics, start, destination):
    # Priority queue with tuples of (estimated total cost, actual cost, current city, path list)
    priorityQueue = [(heuristics[start], 0, start, [start])]
    visited = set()  # Track visited nodes

    while priorityQueue:
        estimatedTotalCost, actualCost, current, path = heapq.heappop(priorityQueue)

        if current in visited:  # Skip if already visited
            continue
        visited.add(current)

        if current == destination:  # Goal test
            outFile.write(f"Path: {' -> '.join(path)}\nTotal distance: {actualCost} km")
            return

        # Explore neighbors
        for neighborInfo in graph[current]:
            neighborCity, distance = neighborInfo
            if neighborCity not in visited:
                newActualCost = actualCost + distance
                estimatedTotalCost = newActualCost + heuristics[neighborCity]
                heapq.heappush(priorityQueue, (estimatedTotalCost, newActualCost, neighborCity, path + [neighborCity]))

    outFile.write("NO PATH FOUND")

inFile = open("Input file.txt", 'r')
outFile = open("output.txt", 'w')

adjacencyList, heuristics, destination = graphHeuristic(inFile)
aStarSearch(adjacencyList, heuristics, "Arad", destination)

inFile.close()
outFile.close()