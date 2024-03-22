import pygame
import algorithms

global node_id


class Node:
  def __init__(self, name, color, pos_x, pos_y, id):
    self.name = name
    self.color = color
    self.pos_x = pos_x
    self.id = id
    self.pos_y = pos_y

  def __eq__(self, other):
        return self.name == other.name and self.color == other.color and \
               self.pos_x == other.pos_x and self.pos_y == other.pos_y and self.id == other.id
  
  def __lt__(self, other):
    return self.name < other.name

  _aboba = 0

class Edge:
  def __init__(self, from_, to_, start_pos: tuple, end_pos: tuple, weight: int = 1):
    self.from_ = from_
    self.to_ = to_
    self.start_pos_x = start_pos[0]
    self.start_pos_y = start_pos[1]
    self.end_pos_x = end_pos[0] 
    self.end_pos_y = end_pos[1]
    self.weight = weight

class Graph:
  def __init__(self):
    self.graph = [[] for i in range(0, 100)]
    self.nodes = []
    self.edges = []

  def AddEdge(self, u: int, v: int, edge: Edge):
    self.graph[u].append(v)
    self.edges.append(edge)
    

  def AddNode(self, node: Node):
    self.nodes.append(node)

  def SaveGraph(self, filename="graph.txt"):
    with open(filename, "w") as file:
      for node in self.nodes:
        file.write(f"{node.name} {node.color} {node.id} {node.pos_x} {node.pos_y}")
        for adj_node in self.graph[node.id]:
          file.write(f" {adj_node}")
        file.write("\n")

  def LoadGraph(self, filename="graph.txt") -> None:
      global node_id
      
      with open(filename, "r") as file:
          lines = file.readlines()
          self.graph = [[] for _ in range(100)]
          self.nodes = []
          self.edges = []
          max_id = -1
          
          for line in lines:
            parts = line.split()
            name, color, id, pos_x, pos_y = parts[:5]
            id = int(id)
            pos_x, pos_y = float(pos_x), float(pos_y)
            node = Node(name, color, pos_x, pos_y, id)
            self.nodes.append(node)
            max_id = max(max_id, id)
            
            for adj_id_str in parts[5:]:
              adj_id = int(adj_id_str)
              self.graph[id].append(adj_id)
              self.graph[adj_id].append(id)

          for line in lines:
            parts = line.split()
            name, color, id, pos_x, pos_y = parts[:5]
            id = int(id)
            pos_x, pos_y = float(pos_x), float(pos_y)
            
            for adj_id_str in parts[5:]:
              
              adj_id = int(adj_id_str)
              id_to_load = -1
              for i in range(0, len(self.nodes)):
                if (self.nodes[i].id == adj_id):
                  id_to_load = i
                  self.edges.append(Edge(id, adj_id, (pos_x, pos_y), (self.nodes[i].pos_x, self.nodes[i].pos_y)))
          node_id = max_id + 1
      self.graph = [[] for i in range(0, 49)]
      for edge in self.edges:
        self.graph[edge.from_].append(edge.to_)
      self.max_id = max_id
  global id
  id = 0

mouse_pos_x = 0
mouse_pos_y = 0

def ScreenToWorld(screen_x, screen_y, offset_x, offset_y, zoom):
    world_x = (screen_x - offset_x) / zoom
    world_y = (screen_y - offset_y) / zoom
    return world_x, world_y

def WorldToScreen(world_x, world_y, offset_x, offset_y, zoom):
    screen_x = (world_x * zoom) + offset_x
    screen_y = (world_y * zoom) + offset_y
    return screen_x, screen_y

def DrawEditorInfo(screen, font, insert_mode: bool):
  img = font.render("INSERT" if (insert_mode) else "NORMAL", True, "black")
  rect = img.get_rect()
  screen.blit(img, (20, 680))

def UpdateInsertMode(keys, insert_mode: bool, was_changed: bool):
  if keys[pygame.K_i] and not was_changed:
    return True, True
  elif keys[pygame.K_ESCAPE] and not was_changed:
    return False, True
  return insert_mode, False

def Solution(graph):
  #номер 1
  print("1:")
  if (algorithms.CheckForBipartite(graph.graph)):
    if (len(graph.edges) / 2 <= 2 * len(graph.nodes) - 3 - 4):
      print("ПЛАНАРНЫЙ")
    else:
      print("НЕПЛАНАРНЫЙ")
  else:
    if (len(graph.edges) / 2 <= 3 * len(graph.nodes) - 3 - 6):
      print(3 * len(graph.nodes) - 3 - 6)
      print("ПЛАНАРНЫЙ")
    else:
      print("НЕПЛАНАРНЫЙ", len(graph.edges), len(graph.nodes))

  #номер 2
  print()
  print("2:")
  print("|V| = ", len(graph.nodes))
  print("|E| = ", len(graph.edges) // 2)
  min_deg = 1000000
  max_deg = -1
  for i in range(len(graph.graph)):
      min_deg = min(min_deg, len(graph.graph[i]))
      max_deg = max(max_deg, len(graph.graph[i]))
  print("Min deg: ", min_deg, ' ', "Max deg: ", max_deg)
  graph_properties = algorithms.FindGraphProperties(graph)
  print("РАДИУС: ", graph_properties.radius)
  print("ДИАМЕТР: ", graph_properties.diameter)
  print("ЦЕНТРЫ: ", *graph_properties.centers)
  print("ЦИКЛОМАТИЧЕСКОЕ ЧИСЛО: ", int(graph_properties.cyclomatic_num))

  #номер 3
  algorithms.ColorTheGraph(graph)
  print("ХРОМАТИЧЕСКОЕ ЧИСЛО: ", 4)

  #номер 5
  print("6 ВИСЯЧИХ ВЕРШИН: ДАНИЯ, ИРЛАНДИЯ, ПОРТУГАЛИЯ, МОНАКО, ВАТИКАН, МОНАКО")

  #6
  print("ДВУДОЛЬНЫЙ")

  #prufer uncomment if needed
  # prufer = algorithms.PruferCode(graph)
  # for i in range(len(prufer)):
  #   for j in range(len(graph.nodes)):
  #     if (graph.nodes[j].id == prufer[i]):
  #       print(graph.nodes[j].name, end = ' ')


def main():
  pygame.init()
  global node_id
  node_id = 0
  font = pygame.font.Font("res/0xProtoNerdFont-Regular.ttf", 12)

  screen = pygame.display.set_mode((1280, 720))
  clock = pygame.time.Clock()
  running = True

  graph = Graph()
  graph.LoadGraph()
  
  Solution(graph)

  insert_mode, was_changed = False, False
  is_created = False
  is_dragging_camera = False
  is_drawing_edge = False
  is_new_line = False
  is_dragging_node = False
  dragged_node = None
  selected_nodes = []
  offset_x = 0
  offset_y = 0
  zoom = 1.0
  start_pos_x, start_pos_y = 0, 0
  end_pos_x, end_pos_y = 0, 0
  from_, to_ = None, None
  selected_start_x, selected_start_y = None, None
  selected_end_x, selected_end_y = None, None

  node = Node("a", "blue", 1, 2, 3)
  node._aboba = 2
  while (running):
    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
        running = False
      elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 2 and (not insert_mode)):
        is_dragging_camera = True
        print("YES")
        start_drag_x, start_drag_y = pygame.mouse.get_pos()
      elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (not insert_mode)):
        current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
        current_mouse_x, current_mouse_y = ScreenToWorld(current_mouse_x, current_mouse_y, offset_x, offset_y, zoom)
        selected_start_x, selected_start_y= pygame.mouse.get_pos()
        selected_start_x, selected_start_y = ScreenToWorld(selected_start_x, selected_start_y, offset_x, offset_y, zoom)
        for node in graph.nodes:
          if (current_mouse_x >= node.pos_x - 23 * zoom and current_mouse_x <= node.pos_x + 23 * zoom and
              current_mouse_y >= node.pos_y - 23 * zoom and current_mouse_y <= node.pos_y + 23 * zoom):
            dragged_node = node
            is_dragging_node = True
            break
      
      elif (event.type == pygame.MOUSEBUTTONUP and event.button == 1 and (not insert_mode)):
        selected_end_x, selected_end_y = pygame.mouse.get_pos()
        selected_end_x, selected_end_y = ScreenToWorld(selected_end_x, selected_end_y, offset_x, offset_y, zoom)
        if (abs(selected_end_x - selected_start_x) <= 5 and abs(selected_end_y - selected_start_y) <= 5):
          for node in graph.nodes:
            if (selected_start_x >= node.pos_x - 23 * zoom and selected_start_x <= node.pos_x + 23 * zoom and
                selected_start_y >= node.pos_y - 23 * zoom and selected_start_y <= node.pos_y + 23 * zoom):
              node.color = "red"
              if (node not in selected_nodes):
                selected_nodes.append(node)
              break
        is_drawing_edge = False
        selected_start_x, selected_start_y = None, None
        selected_end_x, selected_end_y = None, None
        is_dragging_node = False
        dragged_node = None

      elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and insert_mode):
        
        is_new_line = True
        if (is_new_line):
          start_pos_x, start_pos_y = pygame.mouse.get_pos()
          start_pos_x, start_pos_y = ScreenToWorld(start_pos_x, start_pos_y, offset_x, offset_y, zoom)
          is_new_line = False
        
        for node in graph.nodes:
          
          if ((start_pos_x >= node.pos_x - 23 * zoom and start_pos_x <= node.pos_x + 23 * zoom) and
              (start_pos_y >= node.pos_y - 23 * zoom and start_pos_y <= node.pos_y + 23 * zoom)):
            start_pos_x = node.pos_x
            start_pos_y = node.pos_y
            from_ = node
            is_drawing_edge = True
            break
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
          graph.SaveGraph()
      elif (event.type == pygame.MOUSEBUTTONUP and event.button == 1 and insert_mode):
        current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
        current_mouse_x, current_mouse_y = ScreenToWorld(current_mouse_x, current_mouse_y, offset_x, offset_y, zoom)
        for node in graph.nodes:
                  
          if ((current_mouse_x >= node.pos_x - 23 * zoom and current_mouse_x <= node.pos_x + 23 * zoom) and
              (current_mouse_y >= node.pos_y - 23 * zoom and current_mouse_y <= node.pos_y + 23 * zoom)):
            end_pos_x = node.pos_x
            end_pos_y = node.pos_y
            to_ = node
            print(from_.id, ' ', to_.id)
            graph.graph[to_.id].append(from_.id)
            graph.AddEdge(from_.id, to_.id, Edge(from_.id, to_.id, (start_pos_x, start_pos_y), (end_pos_x, end_pos_y)))
            break
        
        is_drawing_edge = False
      
      elif (event.type == pygame.MOUSEBUTTONUP and event.button == 2):
        is_dragging_camera = False
        print("NO")
      elif (event.type == pygame.MOUSEBUTTONDOWN):
        if (event.button == 4):
          zoom *= 1.1
          offset_x = (offset_x - screen.get_width() / 2) * 1.1 + screen.get_width() / 2
          offset_y = (offset_y - screen.get_height() / 2) * 1.1 + screen.get_height() / 2
        elif (event.button == 5):
          zoom *= 0.9
          offset_x = (offset_x - screen.get_width() / 2) * 0.9 + screen.get_width() / 2
          offset_y = (offset_y - screen.get_height() / 2) * 0.9 + screen.get_height() / 2
      if (insert_mode and event.type == pygame.MOUSEBUTTONUP and event.button == 3):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()

        mouse_world_pos_x, mouse_world_pos_y = ScreenToWorld(mouse_pos_x, mouse_pos_y, offset_x, offset_y, zoom)
        name_pos_x, name_pos_y = mouse_pos_x - 25, mouse_pos_y + 25
        is_capturing_name = True
        is_success = True
        node_name = ''

        while (is_capturing_name):
          screen.fill((173, 216, 230))
          
          for event in pygame.event.get():
            if (event.type == pygame.QUIT):
              is_capturing_name = False
              running = False
            if (event.type == pygame.KEYDOWN):
              if (event.key == pygame.K_ESCAPE):
                is_capturing_name = False
                is_success = False

              if (event.key == pygame.K_RETURN):
                is_capturing_name = False
              elif (event.key == pygame.K_BACKSPACE):
                node_name = node_name[:-1]
              else:
                node_name += event.unicode

          name_text = font.render(node_name, True, "black")
          screen.blit(name_text, (name_pos_x, name_pos_y))

          for node in graph.nodes:
            node_screen_pos = WorldToScreen(node.pos_x, node.pos_y, offset_x, offset_y, zoom)
            pygame.draw.circle(screen, node.color, node_screen_pos, int(23 * zoom))
            text_surface = font.render(node.name, True, "black")
            screen.blit(text_surface, (node_screen_pos[0] - 25 * zoom, node_screen_pos[1] + 25 * zoom))

          new_node_screen_pos = WorldToScreen(mouse_world_pos_x, mouse_world_pos_y, offset_x, offset_y, zoom)
          pygame.draw.circle(screen, "blue", new_node_screen_pos, 23 * zoom)

          pygame.display.flip()

        if (is_success):
          
          new_node = Node(node_name, "blue", mouse_world_pos_x, mouse_world_pos_y, node_id)
          node_id += 1
          print(new_node.id)
          print("ADDED: ", new_node.name)
          graph.AddNode(new_node)
          print(node_name)

      if (is_dragging_camera):
        current_drag_x, current_drag_y = pygame.mouse.get_pos()  
        offset_x += current_drag_x - start_drag_x
        offset_y += current_drag_y - start_drag_y
        start_drag_x = current_drag_x
        start_drag_y = current_drag_y


      
    screen.fill((173, 216, 230))

    if (is_dragging_node):
      mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
      dragged_node.pos_x, dragged_node.pos_y = ScreenToWorld(mouse_pos_x, mouse_pos_y, offset_x, offset_y, zoom)
      
      for edge in graph.edges:
        if (edge.from_ == dragged_node.id):
          edge.start_pos_x, edge.start_pos_y = dragged_node.pos_x, dragged_node.pos_y
        elif (edge.to_ == dragged_node.id):
          edge.end_pos_x, edge.end_pos_y = dragged_node.pos_x, dragged_node.pos_y

    if is_drawing_edge:
      current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
      
      start_screen_x, start_screen_y = WorldToScreen(start_pos_x, start_pos_y, offset_x, offset_y, zoom)
      
      pygame.draw.line(screen, "black", (start_screen_x, start_screen_y), (current_mouse_x, current_mouse_y), int(5 * zoom))


    for edge in graph.edges:
      edge_start_screen_pos = WorldToScreen(edge.start_pos_x, edge.start_pos_y, offset_x, offset_y, zoom)
      edge_end_screen_pos = WorldToScreen(edge.end_pos_x, edge.end_pos_y, offset_x, offset_y, zoom)
      pygame.draw.line(screen, "black", edge_start_screen_pos, edge_end_screen_pos, int(5 * zoom))
    for node in graph.nodes:
      node_screen_pos = WorldToScreen(node.pos_x, node.pos_y, offset_x, offset_y, zoom)
      pygame.draw.circle(screen, node.color, node_screen_pos, int(23 * zoom))
      text_surface = font.render(node.name, True, "black")
      screen.blit(text_surface, (node_screen_pos[0] - 25 * zoom, node_screen_pos[1] + 25 * zoom))



    text_surface = font.render("False" if (not insert_mode) else "True", True, "black")
    screen.blit(text_surface, (20, 20))

    keys = pygame.key.get_pressed()
    
    insert_mode, was_changed = UpdateInsertMode(keys, insert_mode, was_changed)

    DrawEditorInfo(screen, font, insert_mode)

    

    if keys[pygame.K_ESCAPE]:
      for node in graph.nodes:
        node.color = "blue"
    if keys[pygame.K_a]:
      offset_x += 5 * zoom
    if keys[pygame.K_d]:
      offset_x -= 5 * zoom
    if keys[pygame.K_w]:
      offset_y += 5 * zoom
    if keys[pygame.K_s]:
      offset_y -= 5 * zoom

    pygame.display.flip()
    
    clock.tick(60)

if (__name__ == "__main__"):
  main()
