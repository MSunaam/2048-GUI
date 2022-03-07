#importing libraries

#pygame for GUI
import pygame
#random for generating random ints
import random
#for deep copy
import copy
#for delay
import time
#for menu
import pygame_menu
#for colors
from colors import *
#for values
from values import *


#initializing pygame
pygame.init()
#initializing font
pygame.font.init()

#screen creation
screen = pygame.display.set_mode((window_width,window_height), pygame.RESIZABLE)

def game():
    
    #for calculating scores
    global sum
    sum = 0

    #title and icon
    pygame.display.set_caption("2048")
    #loading icon
    icon = pygame.image.load("images/joystick.png")
    #setting icon
    pygame.display.set_icon(icon)

    #RGB BACKGROUND COLOR and update to see changes
    screen.fill((250, 248, 239))
    pygame.display.update()

    # #matrix to represent the tiles
    global matrix
    matrix = list()
    for k in range(4):
            row = list()
            for l in range(4):
                row.append("")
            matrix.append(row)


    #save game func saves in save_file.txt
    def saveGame(temp):    
        for row in range(4):
            for k in range(4):
                if temp[row][k] == "":
                    temp[row][k] = 0               
        save_file = open("save_file.txt","wt")
        for row in temp:
            save_file.write(' '.join([str(a) for a in row]) + ';\n')


    print(matrix)

    # # #for testing
    # matrix = [
    #     [8,2,16,4],
    #     [128,8,4,8],
    #     [1024,512,256,256],
    #     [2,4,"",""]
    #  ]


    #creating fonts for use in program
    font = pygame.font.SysFont(None,80)
    text = pygame.font.SysFont(None,50)
    font_small = pygame.font.SysFont(None,70)
    font_smaller = pygame.font.SysFont(None,50)


    #for creating grid
    grid_bg = pygame.Rect((grid_left,grid_top),(grid_width,grid_height))
    #parameters (surface,color,rect name,0 for filled rect,rounded corners)
    pygame.draw.rect(screen,(187, 172, 159),grid_bg,0,20)

    #top and left margins of inner tiles
    tile_top = 220
    tile_left = 370
    empty_tile_color = (204, 193, 179)

    #generating inner tiles for displaying number tiles
    for k in range(4):
        tile_left = 370
        for l in range(4):
            pygame.draw.rect(screen, empty_tile_color,pygame.Rect((tile_left,tile_top),(100,100)),0,5)
            tile_left += 120
        tile_top += 120

    #for generating random ints
    def randomInt():
        global i; global j; global randomTile
        
        i = random.randint(0,3)
        j = random.randint(0,3)
        #generating i,j matrix value such that it is not occupied already
        count = 0
        for o in range(4):
            for p in range(4):
                if matrix[o][p] != "":
                    count+=1

        while count < 16:
            if matrix[i][j] != "":
                j = random.randint(0,3)
                i = random.randint(0,3)
            else:
                break

        #generating either a 2 or a 4 with 80% 20% bias
        randomTile = random.choices([2,4],weights=[80,20])
    randomInt()

    def newGame():
        global matrix
        for l in range(4):
            for k in range(4):
                matrix[l][k] = ""
        return matrix

    #first 2 tiles will appear automatically

    for o in range(2):
        randomInt()
        matrix[i][j] = randomTile[0]
        tile = pygame.Rect((coordinates[i][j]),(100,100))
        pygame.draw.rect(screen,colorDic[matrix[i][j]],tile,0,5)
        pygame.display.update(grid_bg)

    #for syncing the grid and screen surface
    def updateScreen():

        #drawing over existing
        grid_bg = pygame.Rect((grid_left,grid_top),(grid_width,grid_height))
        #parameters (surface,color,rect name,0 for filled rect,rounded corners)
        pygame.draw.rect(screen,(187, 172, 159),grid_bg,0,20)

        #for score board
        #top margin
        score_top = 80
        #left margin
        score_left = 550
        #score rectangle
        score_rect = pygame.Rect((score_left+30,score_top),(300,70))
        pygame.draw.rect(screen,colorDic['text'],score_rect,0,10)
        score_text = text.render("Score: "+str(sum),True,(255,255,255))
        screen.blit(score_text,(score_left+20+30,score_top+20))
        pygame.display.update(score_rect)

        ##for new game button
        global nb
        new_game = pygame.Rect((score_left-87+20,score_top),(70,70))
        reload_img = pygame.image.load("images/reset.png")
        pygame.draw.rect(screen,colorDic['text'],new_game,0,10)
        nb = screen.blit(reload_img,(score_left-83+20,score_top+3))
        pygame.display.update(new_game)

        ##for save game button
        global sb
        save_game = pygame.Rect((score_left-165+20,score_top),(70,70))
        save_img = pygame.image.load("images/diskette.png")
        pygame.draw.rect(screen,colorDic['text'],save_game,0,10)
        sb = screen.blit(save_img,(score_left-162+20,score_top+3))
        pygame.display.update(save_game)

        ##for new game button
        global lg
        load_game = pygame.Rect((score_left-250+20,score_top),(70,70))
        save_file_img = pygame.image.load("images/loadGame.png")
        pygame.draw.rect(screen,colorDic['text'],load_game,0,10)
        lg = screen.blit(save_file_img,(score_left-245+20,score_top+3))
        pygame.display.update(load_game)

        #tile rects margins and colors
        tile_top = 220
        tile_left = 370
        # empty_tile_color = (204, 193, 179)

        #background grid boxes generation through loop
        for k in range(4):
            tile_left = 370
            for l in range(4):
                tile = pygame.Rect((tile_left,tile_top),(100,100))
                pygame.draw.rect(screen, empty_tile_color,tile,0,5)
                tile_left += 120
            tile_top += 120
        pygame.display.update(grid_bg) #updating only backgorund grid for new tiles to appear

        # new tiles being generated and font appearing
        for k in range(4):
            for l in range(4):
                if matrix[k][l] != "":
                    #new rects
                    tile = pygame.Rect((coordinates[k][l]),(100,100))
                    pygame.draw.rect(screen,colorDic[matrix[k][l]],tile,0,5)
                    if len(str(matrix[k][l])) == 1:
                        ##(render parameters string,antialiasing,color)
                        img = font.render(str(matrix[k][l]),True,colorDic['text'])
                        x,y = coordinates[k][l]
                        x+=33;y+=24
                        screen.blit(img,(x,y))
                    elif len(str(matrix[k][l])) == 2:
                        img = font.render(str(matrix[k][l]),True,colorDic['text'])
                        x,y = coordinates[k][l]
                        x+=17;y+=23
                        screen.blit(img,(x,y))
                    elif len(str(matrix[k][l])) == 3:
                        img = font_small.render(str(matrix[k][l]),True,colorDic['text'])
                        x,y = coordinates[k][l]
                        x+=8;y+=25
                        screen.blit(img,(x,y))
                    elif len(str(matrix[k][l])) == 4:
                        img = font_smaller.render(str(matrix[k][l]),True,colorDic['text'])
                        x,y = coordinates[k][l]
                        x+=11;y+=30
                        screen.blit(img,(x,y))
                    pygame.display.update(tile) #updating only tiles

    #for adding a new tile to grid after each key press
    def newTile():
        count = 0
        #check if there is any empty tile
        for o in range(4):
            for p in range(4):
                if matrix[o][p] != "":
                    count+=1
                

        #for adding a new tile to grid after each move
        if count < 16:
            matrix[i][j] = randomTile[0]
            print(i,j,randomTile[0])
            updateScreen()

    #for checking if the user lost
    def lose():
        for l in range(4):
            for k in range(4):
                if(matrix[l][k]== ""):
                    return False
        for l in range(3):
            for k in range(3):
                if(matrix[l][k]== matrix[l + 1][k] or matrix[l][k]== matrix[l][k + 1]):
                    return False
    
        for k in range(3):
            if(matrix[3][k]== matrix[3][k + 1]):
                return False
    
        for k in range(3):
            if(matrix[k][3]== matrix[k + 1][3]):
                return False

        ## if lose then stop game and print
        print("You Lost!")
        lose_rect = pygame.Surface((grid_width,grid_height), pygame.SRCALPHA)
        lose_rect.fill((250,248,239,128))
        #showing transparent rect
        screen.blit(lose_rect, (grid_left,grid_top))
        lose = font.render("You Lost!",True,colorDic['text'])
        #showing text
        screen.blit(lose,(480,430))
        pygame.display.update(grid_bg)

        return True

    def winfn():
        for l in matrix:
            for k in l:
                if k == 2048:
                    print("you won")
                    win_rect = pygame.Surface((grid_width,grid_height), pygame.SRCALPHA)
                    win_rect.fill((250,248,239,128))
                    screen.blit(win_rect, (grid_left,grid_top))
                    win = font.render("You Won!",True,colorDic['text'])
                    screen.blit(win,(480,430))
                    pygame.display.update(grid_bg)
                    win = False
                    return True

    def loadGame():

        save_file = open("save_file.txt","rt")
        matrix = list()
        for k in range(4):
            temp = list()
            file = save_file.readline()
            file = file.replace(";","")

            temp = file.split()
            matrix.append(temp)

        for k in range(4):
            for l in range(4):
                matrix[k][l] = int(matrix[k][l])
                if matrix[k][l] == 0:
                    matrix[k][l] = ""
        pygame.display.update()

        return matrix
        

    #for while loop
    program_running = True

    updateScreen()

    #for inner while loop
    win = True

    #while loop for pygame window
    while program_running:

        #for exiting when close button pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False



        while win:
            #for exiting when close button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_running = False
                    win = False

                #for new game when new game button clicked
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if nb.collidepoint(pos):
                        matrix = newGame()
                        sum = 0
                        updateScreen()
                        newTile()
                    if sb.collidepoint(pos):
                        temp = copy.deepcopy(matrix)
                        saveGame(temp)
                    if lg.collidepoint(pos):
                        matrix = loadGame()
                    updateScreen()

                        
                #when keyboard button is pressed
                if event.type == pygame.KEYDOWN: 

                    #calling lose function to check if user has lost
                    #if user lost then suspend game wihtout terminating window and display you lose
                    if lose():
                        win = False
                        break

                    ##printing in terminal for testing
                    for l in range(4):
                        print(matrix[l])
                    print(randomTile[0])
                    print()


                    #when left key pressed
                    if event.key == pygame.K_LEFT:
                        #for testing
                        print("left")

                        #moving
                        for k in range(4):
                            for o in range(4):
                                for l in range(3,0,-1):
                                    if matrix[k][l-1]=="":
                                        matrix[k][l-1] = matrix[k][l]
                                        matrix[k][l] = ""                

                        #adding
                        for k in range(4):
                            for l in range(3):
                                if matrix[k][l] == matrix[k][l+1]:
                                    matrix[k][l] += matrix[k][l+1]
                                    matrix[k][l+1] = ""
                                    if matrix[k][l] != "":
                                        sum += matrix[k][l]
                                        

                        #moving
                        for k in range(4):
                            for o in range(4):
                                for l in range(3,0,-1):
                                    if matrix[k][l-1]=="":
                                        matrix[k][l-1] = matrix[k][l]
                                        matrix[k][l] = ""
                                        

                        updateScreen()          
                        

                    #when right key is pressed
                    elif event.key == pygame.K_RIGHT:
                        #print right for testing
                        print("right")

                        #moving
                        for k in range(4):
                            for o in range(4):
                                for l in range(3):
                                    if matrix[k][l+1]=="":
                                        matrix[k][l+1] = matrix[k][l]
                                        matrix[k][l] = "" 
                                        

                        #adding
                        for k in range(4):
                            for l in range(3,0,-1):
                                if matrix[k][l] == matrix[k][l-1]:
                                    matrix[k][l] += matrix[k][l-1]
                                    matrix[k][l-1] = ""  
                                    if matrix[k][l] != "":
                                        sum += matrix[k][l]
                                        

                        #moving
                        for k in range(4):
                            for o in range(4):
                                for l in range(3):
                                    if matrix[k][l+1]=="":
                                        matrix[k][l+1] = matrix[k][l]
                                        matrix[k][l] = ""   
                                        

                        updateScreen()
                        
                    #when up key pressed
                    elif event.key == pygame.K_UP:
                        #for testing print up
                        print("up")

                        #move
                        for l in range(4):
                            for o in range(4):
                                for k in range(3,0,-1):
                                    if matrix[k-1][l] == "":
                                        matrix[k-1][l] = matrix[k][l]
                                        matrix[k][l] = ""        

                        #adding
                        for l in range(4):
                            for k in range(3):
                                if matrix[k][l] == matrix[k+1][l]:
                                    matrix[k][l] += matrix[k+1][l]
                                    matrix[k+1][l] = ""
                                    if matrix[k][l] != "":
                                        sum += matrix[k][l]                                    

                        #move
                        for l in range(4):
                            for o in range(4):
                                for k in range(3,0,-1):
                                    if matrix[k-1][l] == "":
                                        matrix[k-1][l] = matrix[k][l]
                                        matrix[k][l] = ""
                        

                        updateScreen()

                    #when down key is pressed
                    elif event.key == pygame.K_DOWN:
                        #print dow for testing
                        print("down")

                        #moving
                        for l in range(4):
                            for o in range(4):
                                for k in range(3):
                                    if matrix[k+1][l] == "":
                                        matrix[k+1][l] = matrix[k][l]
                                        matrix[k][l] = ""
                                        

                        #add
                        for l in range(4):
                            for k in range(3,0,-1):
                                if matrix[k-1][l] == matrix[k][l]:
                                    matrix[k][l] += matrix[k-1][l]
                                    matrix[k-1][l] = ""
                                    if matrix[k][l] != "":
                                        sum += matrix[k][l]
                                        

                        #moving
                        for l in range(4):
                            for o in range(4):
                                for k in range(3):
                                    if matrix[k+1][l] == "":
                                        matrix[k+1][l] = matrix[k][l]
                                        matrix[k][l] = ""
                                        

                        updateScreen()


                    if (event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP):
                            # #generating new random ints for new tiles
                            randomInt()
                            #for testing printing i,j
                            print(i,j)
                            #delaying for 1 sec to see changed moves before new tile appears
                            time.sleep(0.09)
                            #generating new tile updating in matrix
                            newTile()

                    ##if 2048 tile exists then user wins
                    if winfn():
                        win = False
                        break


                    ##for testing
                    for l in range(4):
                        print(matrix[l])
                    print()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_running = False

                #for new game when new game button clicked
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if nb.collidepoint(pos):
                        matrix = newGame()
                        sum = 0
                        updateScreen()
                        newTile()
                        win = True
                    if lg.collidepoint(pos):
                        matrix = loadGame()
                        win = True
                    updateScreen()

menu = pygame_menu.Menu('Welcome to 2048', window_width, window_height,theme=pygame_menu.themes.THEME_SOLARIZED)
menu.add.button('Play', game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
