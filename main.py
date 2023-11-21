import pygame
from pygame.math import Vector2
pygame.font.init()
import numpy as np
from Scripts.Grid import Grid
from Scripts.Dijkstra import Dijkstra

resolution = Vector2(1500, 900)
WIN = pygame.display.set_mode((int(resolution.x), int(resolution.y)))
pygame.display.set_caption("Pathfinding Visualizer")

FPS_Font = pygame.font.SysFont('sans-serif', 40)

def draw_window(TimePerFrame):
    WIN.fill((20, 80, 145))
    grid.draw(WIN)
    drawlines(WIN)
    drawFPS(TimePerFrame)
    pygame.display.update()
    
    
def getFPS(TimePerFrame):
    return round(1 / TimePerFrame)

def drawFPS(TimePerFrame):
    CurrentFPS = getFPS(TimePerFrame)
    FPS_Text = FPS_Font.render("FPS: "  + str(CurrentFPS), 1, (255, 255, 255))
    WIN.blit(FPS_Text, (int(resolution.x) - 150, 10))
    
gridDimensions = [150, 90] #rows, columns
nodeDimensions = [resolution[0]/gridDimensions[0], resolution[1]/gridDimensions[1]]
grid = Grid(gridDimensions[0], gridDimensions[1], nodeDimensions, Vector2(0,0), Vector2(4,4))
    
def drawlines(surface):
    lineColor = (20, 70, 145)
    for i in range(gridDimensions[1]+1):
        pygame.draw.line(surface, lineColor,
                        (0, int(i * nodeDimensions[1])),
                        (int(gridDimensions[0] * nodeDimensions[0]),int(i * nodeDimensions[1])))
    for i in range(gridDimensions[0]+1):
        pygame.draw.line(surface, lineColor,
                        (int(i * nodeDimensions[0]), 0),
                        (int(i * nodeDimensions[0]),int(gridDimensions[1] * nodeDimensions[1])))
    

def main():
    clock = pygame.time.Clock()
    running = True
    algorithmComplete = False
    blocks = {"S": "start", "E": "end", "W": "wall", "G": "weight"}
    weight = 5
    mouseHold = False
    selectedBlock = "wall"
    timePassed = 0
    speed = 1
    currentAnimatedNode = None
    while running:
        TimePerFrame  = clock.tick(300) * .001
        dt = TimePerFrame
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            keysPressed = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keysPressed[pygame.K_s]:
                    selectedBlock = blocks["S"]
                if keysPressed[pygame.K_e]:
                    selectedBlock = blocks["E"]
                if keysPressed[pygame.K_w]:
                    selectedBlock = blocks["W"]
                if keysPressed[pygame.K_g]:
                    selectedBlock = blocks["G"]
                if keysPressed[pygame.K_r]:
                    algorithmComplete = False
                    grid.reset()
                if keysPressed[pygame.K_SPACE]:
                    if not algorithmComplete:
                        visitedNodesInOrder, shortestPath = Dijkstra(grid)
                        algorithmComplete = True
                        timePassed = 0
                        dt = 0
                    else:
                        algorithmComplete = False
                        grid.reset()
        
        if keysPressed[pygame.K_UP]:
            speed += 1
        if keysPressed[pygame.K_DOWN]:
            if speed > 1:
                speed -= 1
                
        mousePosition = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        if mousePressed[0]:
            if algorithmComplete:
                algorithmComplete = False
                grid.reset()
                    
            selectedNode = grid.getPressedNode(mousePosition)
            if not (selectedNode.isEnd or selectedNode.isStart):
                if not selectedNode.isWall:
                    if selectedBlock == "start":
                        grid.changeStartNode(selectedNode)
                    if selectedBlock == "end":
                        grid.changeEndNode(selectedNode)
                    
                if selectedBlock == "wall":
                    if not mouseHold:
                        selectedState = not selectedNode.isWall
                    if selectedNode.weight and selectedState:
                        selectedNode.weight = 0
                    selectedNode.isWall = selectedState
                    
                if selectedBlock == "weight":
                    if not mouseHold:
                        if selectedNode.weight != weight:
                            selectedState = True
                        else:
                            selectedState = False
                    if selectedState and not selectedNode.isWall:
                        selectedNode.weight = weight
                    else:
                        selectedNode.weight = 0
            mouseHold = True
        else:
            mouseHold = False
                
        
        if algorithmComplete:
            timePassed += dt
            ticks = int(timePassed // (1/speed))
            if ticks:
                timePassed %= (1/speed)
                for tick in range(ticks):
                    if len(visitedNodesInOrder) or len(shortestPath):
                        if len(visitedNodesInOrder):
                            if currentAnimatedNode:
                                currentAnimatedNode.isSelected = False
                            currentAnimatedNode = visitedNodesInOrder[0]
                            visitedNodesInOrder = np.delete(visitedNodesInOrder, 0)
                            currentAnimatedNode.animated = True
                        elif len(shortestPath):
                            currentAnimatedNode = shortestPath[-1]
                            currentAnimatedNode.isPath = True
                            shortestPath = np.delete(shortestPath, -1)
                        currentAnimatedNode.isSelected = True
                
                    
        draw_window(TimePerFrame)

    pygame.quit()
    
if __name__ == "__main__":
    main()