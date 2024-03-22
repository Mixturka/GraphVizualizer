import queue
from itertools import *
from bisect import *

class GraphProperties:
  def __init__(self, radius: int, diameter: int, centers: list, cyclomatic_num: int):
    self.radius = radius
    self.diameter = diameter
    self.centers = centers
    self.cyclomatic_num = cyclomatic_num

def CheckForBipartite(graph: list) -> None:
	colors = [-1 for _ in range(0, len(graph))]
	
	def DFS(v, prev_color) -> bool:
		nonlocal colors
		colors[v] = 1 if (prev_color == 2) else 2

		for u in graph[v]:
			if (colors[u] == -1):
				if (not DFS(u, colors[v])):
					return False
			elif (colors[u] == colors[v]):
				return False
			
		return True
	
	for v in range(0, len(graph)):
		if (colors[v] == -1):
			if (not DFS(v, 2)):
				return False
			
		return True

def FindGraphProperties(graph) -> GraphProperties:

	def GetConnectedComponents(graph: list) -> list:
		visited = [False] * len(graph)
		components = []

		def Visit(v: int, component: list):
			visited[v] = True
			component.append(v)

			for u in graph[v]:
				if not visited[u]:
						Visit(u, component)

		for i in range(len(graph)):
			if not visited[i]:
				component = []
				Visit(i, component)
				components.append(component)

		return components

	components = GetConnectedComponents(graph.graph)

	suggested_radiuses = [1e9] * len(graph.graph)
	suggested_diameters = [-1] * len(graph.graph)

	def BFS(graph: list, src: int) -> int:
		dist = [1e9] * len(graph)
		q = queue.Queue()

		dist[src] = 0
		q.put(src)

		while not q.empty():
			node = q.get()

			for neighbour in graph[node]:
				if dist[neighbour] == 1e9:
					dist[neighbour] = dist[node] + 1
					q.put(neighbour)
			
		return max(d for d in dist if d != 1e9)

	for component in components:
		if len(component) > 1:
			for node in component:
				eccentricity = BFS(graph.graph, node)
				if (eccentricity < suggested_radiuses[node]):
					suggested_radiuses[node] = eccentricity
				if (eccentricity > suggested_diameters[node]):
					suggested_diameters[node] = eccentricity

	overall_radius = min(suggested_radiuses)
	overall_diameter = max(suggested_diameters)

	centers = [node.name for node in graph.nodes for d in range(len(graph.graph)) \
            if node.id == d and suggested_radiuses[d] == overall_radius]

	cyclomatic_number = len(graph.edges) // 2 - len(graph.nodes) + len(components)

	return GraphProperties(overall_radius, overall_diameter, centers, cyclomatic_number)

def ColorTheGraph(graph) -> None:
  colors = ["blue", "yellow", (255, 140, 0), (0, 150, 0)]

  result = [-1] * len(graph.nodes)
  result[0] = 0

  for node_index in range(1, len(graph.nodes)):
    available = [True] * len(colors)

    for neighbor_index in graph.graph[node_index]:
      if result[neighbor_index] != -1:
        available[result[neighbor_index]] = False

    for color_index, color_available in enumerate(available):
      if color_available:
        result[node_index] = color_index
        break

  for node_index, node in enumerate(graph.nodes):
    node.color = colors[result[node_index]]

def PruferCode(graph):
    if not graph.nodes:
      return []

    degree = [0] * len(graph.nodes)
    for node_id in range(len(graph.nodes)):
      degree[node_id] = len(graph.graph[node_id])

    prufer_code = []

    for _ in range(len(graph.nodes) - 2):
      for i in range(len(graph.nodes)):
        if degree[i] == 1:
          leaf = i
          break

      for j in range(len(graph.nodes)):
        if leaf in graph.graph[j]:
          neighbor = j
          break

      prufer_code.append(graph.nodes[neighbor].id)

      degree[leaf] -= 1
      degree[neighbor] -= 1
      graph.graph[neighbor].remove(leaf)
      graph.graph[leaf] = []

    return prufer_code