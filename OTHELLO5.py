#Othello game

import pygame , sys, time, subprocess                       #imports pygame libraries
from copy import deepcopy                                   #import from libraries deepcopy
pygame.init()                                               #pygame is initallised

screen = pygame.display.set_mode((1200, 800))               #Screen is sized to 1200x800 pixels
pygame.display.set_caption('Othello')                       #Given name to the game window
green = (0, 150, 0)
black = (0, 0, 0)
white = (255, 255, 255)
done = False                                                #boolean variable that will enable us to terminate the loop when user presses
                                                            #the cross on the window button
clock = pygame.time.Clock ()                                #manages the speed of the update

#---Fonts used in the game---#
fontTitle = pygame.font.Font (None, 60)
font = pygame.font.Font(None, 50)

 
frame_count = 0
frame_rate = 20




def drawGrid():                                             #function that will draw 8 vertical and horizontal lines
    for x in range (10, 730, 80):                           #to create a 8x8 game board with square length of 80 px
        pygame.draw.line (screen, black, (x, 10),(x, 650))  
    for y in range (10, 730, 80):
        pygame.draw.line (screen, black, (10,y),(650, y))



class Hand (pygame.sprite.Sprite):                                  #class that loads an image of a cursor when it is on a button
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)                         #Function that creates a surface on which the imigame of a hand 
        handImage = pygame.image.load ('pointer.png').convert()     #will occur
        self.image = pygame.Surface ([20,20])
        self.image.set_colorkey (white)
        self.image.blit (handImage, (0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 388
        self.rect.y = 190

    def moveHand (self, mousePosition):                             #function that gets the x,y coordinates of a mouse so that it is               
        self.rect.x = mousePosition [0]                             #possible to move with the hand
        self.rect.y = mousePosition [1]

hand1 = Hand ()                                              #creation of an instance of a button (hand) cursor
hand = pygame.sprite.Group()                                 #creating a pygame group so that we can use already written function draw from 
                                                             #pygame library to change cursor when hovered over the button area
hand.add (hand1)                                             #adding instance hand1 to the group

class Button (pygame.sprite.Sprite):                        #creating a class Button where will be described all function needed for working button

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
    def drawRect (self,x,y):                                #function that is used to draw a button
        pygame.draw.rect (screen, black, (x,y,125,75), 5)   

    def cursor (self, mousePosition):                       #function that will change the mouse cursor into a hand when the mouse is hovered over the
                                                            #button to make obvious that it is a button
        pygame.mouse.set_visible (True)                     
        
        if 750+125 > mousePosition[0]> 750 and 500+75 > mousePosition [1] > 500:    #restricts areas of the four buttons 
            pygame.mouse.set_visible (False)                                        #turns off the mouse cursor and changes it into the hand  
            hand.draw (screen)

        if 750+125 > mousePosition[0]> 750 and 640+75 > mousePosition [1] > 640:
            pygame.mouse.set_visible (False)                
            hand.draw (screen)

        if 1000+125 > mousePosition[0]> 1000 and 500+75 > mousePosition [1] > 500:
            pygame.mouse.set_visible (False)                
            hand.draw (screen)

        if 1000+125 > mousePosition[0]> 1000 and 640+75 > mousePosition [1] > 640:
            pygame.mouse.set_visible (False)                
            hand.draw (screen)

    def heading (self,x):                                           #function that displays heading names of the buttons
        if x == 'score':
            scoreHead1 = font.render ('Best', 1, black)
            scoreHead2 = font.render ('Scores',1,black)
            screen.blit (scoreHead1, (755,505))
            screen.blit (scoreHead2, (755, 540))
        if x == 'new_game':
            new_gameHead1 = font.render ('New', 1, black)
            new_gameHead2 = font.render ('Game',1,black)
            screen.blit (new_gameHead1, (1010,505))
            screen.blit (new_gameHead2, (1010, 540))
        if x == 'help':
            helpHead = font.render ('Help', 1, black)
            screen.blit (helpHead, (1025,665))
        if x =='undo':
            undoHead = font.render ('Undo', 1, black)
            screen.blit (undoHead, (770,665))


    def event_handler(self, event, mousePosition, grid, player, frame_count, list_of_moves, no_of_moves, game):
        #function that decides what button was clicked so that the respective function can be done
            
        if 750+125 > mouse[0]> 750 and 500+75 > mouse [1] > 500: #BEST PLAYERS #when clicked it opens text file Bestscores in notepad
            subprocess.call(['notepad.exe', 'BestScores.txt'])      #in a new window



        if 750+125 > mouse[0]> 750 and 640+75 > mouse [1] > 640: #UNDO  #every time the undo button is clicked the game is returned one move back

            if no_of_moves>0: #condition needed to make sure that it is still possible to do undo and it is not already at initial position

                pygame.draw.rect (screen, green, (10,10,690,690),0) #drawing green rectangular and than the grid so that the new position of stones can
                drawGrid()                                          #be drawn
                index = no_of_moves -1
                undo_grid = deepcopy(list_of_moves[index])          #gets the previous stone positions 
                grid = undo_grid                                    #updating the grid variable that holds the stone positions
               
                no_of_moves = no_of_moves -1                        #reducing the number of moves

                drawStones (undo_grid)                              #calling a function that will draw the stones

                zeros=0
                for j in range (8):             #it goes through every square in the grid and if there is free square it adds one to variable
                    for i in range (8):         #to variable zero
                        if grid[j][i]==0:
                            zeros = zeros+1

                #change of the player 
                if zeros!=0:                    #if zeros is not 0 it means that the board is not full and the change of players is neccessary
                    if player =='b':            #if zeros is 0 than it means that the board is full and the change should be skipped until next
                        player = 'w'            #undo press
                        pygame.draw.circle(screen, green, (770,190), 20, 0)
                        pygame.draw.circle(screen, white, (770,30), 20, 0)

                    else:
                        player = 'b'
                        pygame.draw.circle(screen, green, (770,30), 20, 0)
                        pygame.draw.circle(screen, black, (770,190), 20, 0)


                game = True                                           #set the game to True value as it can continue at least one more move
                pygame.draw.rect (screen, green, (100,675,500,100),0) #redraw the statement of the winner in case it is neccessary                   


        if 1000+125 > mouse[0]> 1000 and 500+75 > mouse [1] > 500: #NEW GAME #every time the new game button is clicked the stones are returned to 
                                                                   #initial position and the time starts from zero again
            #reseting of the game window
            grid = [[0 for x in range(8)] for y in range(8)]        #creating clear grid variable with initial stone positions and player
            player='b'

            grid[3][3]='w'
            grid[3][4]='b'
            grid[4][3]='b'
            grid[4][4]='w'
            
            screen.fill (green)                                     #setting background colour
            drawGrid ()                                             #draw a game board grid
            startScore ()                                           #calling function that will display initial score
            drawStones (grid)                                       #calling function that will draw the initial stones 


            screen.blit (titleWhite, (800,10))                      #Displaying titles for white & black score
            screen.blit (titleBlack, (800,170))                     
            screen.blit (time, (700,330))                           #Displaying title for game timer

            pygame.draw.circle(screen, black, (770,190), 20, 0)     #draw black circle next to Black Score heading to indicate that the starting 
                                                                    #player is black
            frame_count = 0                                         #sets frame_count to 0 
            no_of_moves=0                                           #sets number of moves to 0           
            game = True                                             #sets boolean game to True so that moves can be done

        if 1000+125 > mousePosition[0]> 1000 and 640+75 > mousePosition [1] > 640: #RULES #when clicked on help button the rules
                                                                                   #will display in another window
            subprocess.call(['notepad.exe', 'Othello_rules.txt'])


        return grid, player, frame_count, list_of_moves, no_of_moves, game

#initalization of individual buttons            
scoreBut = Button()
new_gameBut = Button ()
ruleBut = Button ()
undoBut = Button ()


radius =[[((10+40+x*80),(10+40+y*80)) for x in range(8)] for y in range (8)]    #2D array that consists of centers of stones for each square respectively
                                                                                #global variable as it does not change 
grid = [[0 for x in range(8)] for y in range(8)]            #2D array that will remember current stones in the grid

player='b'                                                  #starting player will be always black

grid[3][3]='w'                                              #initial spacing of the stones
grid[3][4]='b'
grid[4][3]='b'
grid[4][4]='w'

no_of_moves = 0                                       #sets number of moves to 0
list_of_moves = [0 for a in range (64)]               #create a list that will hold the individual stages of the game
grid_init=[[0 for x in range(8)] for y in range(8)]   #create 2D array that will hold the initial position of stones
grid_init[3][3]='w'
grid_init[3][4]='b'
grid_init[4][3]='b'
grid_init[4][4]='w'

list_of_moves[0]=grid_init                            #assign the initial spacing to first index in the list of moves

def move (grid, mousePosition, player, list_of_moves, no_of_moves): #function that will remember current stage of a game, look if there is still possibility
                                                                    #to move for the player and validate the moves

    valid_list = [0,0,0,0,0,0,0,0]
    valid = False
    if 10<= mousePosition [0] <= 650 and 10<= mousePosition [1] <= 650: #restriction that the function will run only if it was clicked in this area
        squareX = mousePosition[0]//80                                  #identification of the square
        squareY = mousePosition[1]//80

        if squareX==8:
            squareX=7
        if squareY==8:
            squareY=7

        if grid[squareY][squareX]==0:                                   #condition for entering the stone (only when there is no other stone) 

            if player == 'b':                                           #for black player - calling function that makes sure that the place where the player
                checkDown(squareY,squareX, player, grid, valid_list)    #wants to put a stone is allowed
                checkUp(squareY,squareX, player, grid, valid_list)
                checkRight(squareY,squareX, player, grid, valid_list)
                checkLeft(squareY,squareX, player, grid, valid_list)
                checkLeftUp(squareY,squareX, player, grid, valid_list)
                checkLeftDown(squareY,squareX, player, grid, valid_list)
                checkRightUp(squareY,squareX, player, grid, valid_list)
                checkRightDown(squareY,squareX, player, grid, valid_list)
                for i in range (0,8):
                    if valid_list[i] == 1:
                        valid = True
                if valid == True:                                       #if the move is valid than it changes the player
                    player = 'w'
                    pygame.draw.circle(screen, green, (770,190), 20, 0)
                    pygame.draw.circle(screen, white, (770,30), 20, 0)

                    no_of_moves = no_of_moves +1                        #and increase by one number of moves
                
            else:                                                       #the same is done for white player
                checkDown(squareY,squareX, player, grid, valid_list)
                checkUp(squareY,squareX, player, grid, valid_list)
                checkRight(squareY,squareX, player, grid, valid_list)
                checkLeft(squareY,squareX, player, grid, valid_list)
                checkLeftUp(squareY,squareX, player, grid, valid_list)
                checkLeftDown(squareY,squareX, player, grid, valid_list)
                checkRightUp(squareY,squareX, player, grid, valid_list)
                checkRightDown(squareY,squareX, player, grid, valid_list)
                for i in range (0,8):
                    if valid_list[i] == 1:
                        valid = True
                if valid == True:
                    player = 'b'            
                    pygame.draw.circle(screen, green, (770,30), 20, 0)
                    pygame.draw.circle(screen, black, (770,190), 20, 0)

                    no_of_moves = no_of_moves +1


    possible_list = [0,0,0,0,0,0,0,0]                                   #possible list is used to identify whether or not there is a possible move 
    possible = False                                                    #for that player or if it should change the player
    for j in range (8):
        for i in range (8):                                             #it is done by going through all possibilities if there's possibility to make
            Down(j,i, player, grid, possible_list)                      #a move than 0 changes to 1 and players are not switched
            Up(j,i, player, grid, possible_list)
            Right(j,i, player, grid, possible_list)
            Left(j,i, player, grid, possible_list)
            LeftUp(j,i, player, grid, possible_list)
            LeftDown(j,i, player, grid, possible_list)
            RightUp(j,i, player, grid, possible_list)
            RightDown(j,i, player, grid, possible_list)
            for p in range (0,8):
                if possible_list[p] == 1:
                    possible = True

    if possible == False:                                           #if boolean variable possible stayes False than the players (and the indicator 
        if player == 'b':                                           #whose turn it is) are switched
            player='w'
            pygame.draw.circle(screen, green, (770,190), 20, 0)
            pygame.draw.circle(screen, white, (770,30), 20, 0)
        else:
            player ='b'
            pygame.draw.circle(screen, green, (770,30), 20, 0)
            pygame.draw.circle(screen, black, (770,190), 20, 0)

    list_of_moves [no_of_moves]=deepcopy(grid)                      #to the list of moves is added another stage of game under index which is equal to
                                                                    #deepcopy function is used here so that the stages are not overwritten when another
                                                                    #stone is added to grid array
    return player, grid, valid, list_of_moves, no_of_moves


def drawStones (grid):                                                  #function that draws stones onto the the window grid
    for j in range (8):                                                 #it goes through every index in the grid and draws nothing when it is 0,
        for i in range (8):                                             
            if grid[j][i]=='w':                                         #draws white circle if it is 'w'
                pygame.draw.circle(screen, white, radius[j][i], 35, 0)
            if grid[j][i]=='b':                                         #and draws black circle if it is 'b'
                pygame.draw.circle(screen, black, radius[j][i], 35, 0)


def score (grid):                                               #functino that counts the score of the game by calculation number of stones of each color
    pygame.draw.rect (screen, green, (910,60,125,75), 0)        #draws green rectangle over the old score
    pygame.draw.rect (screen, green, (910,220,125,75), 0)
    white_score = 0                                             #in the beginning the score is 0 for both players
    black_score = 0

    for j in range (8):                                         #it goes through every square in the grid and if there is stone one point is added to the
        for i in range (8):                                     #current score (apparent to the color)
            if grid[j][i]=='w':
                white_score = white_score+1
            if grid[j][i]=='b':
                black_score=black_score+1

    score_W = font.render (str(white_score), 1, black)      #writing the updated score to the screen
    score_B = font.render (str(black_score), 1, black)

    screen.blit (score_W, (910,60))
    screen.blit (score_B, (910,220))

    return white_score, black_score


game = True                                             #boolean variable that indicates whether the game is still on or whether is finished
def winner (white_score, black_score, grid, game):                    #function that terminates the game
    whites = 0
    blacks = 0
    zeros = 0
    for j in range(0,8):                                        #done by calculating how many zeros, black and white stones there are in the grid
        for i in range (0,8):
            if grid[j][i] == 'w':
                whites = whites+1
            if grid[j][i]=='b':
                blacks=blacks+1
            if grid[j][i] == 0:
                zeros = zeros+1
    if whites == 0:                                             #in case that one of the player lost all his stones and cant do any other move                                           
        winner = font.render ('Winner is black', 1, black)      #the winner is the one who has the stones
        screen.blit (winner, (200,700))
        game = False
    if blacks == 0:
        winner = font.render ('Winner is white', 1, black)
        screen.blit (winner, (200,700))
        game = False
    if zeros == 0:                                              #if all squares are full than it asks if there are more white or black stones and 
        game = False
        if white_score<black_score:                             #displays the winner
            winner = font.render ('Winner is black', 1, black)
            screen.blit (winner, (200,700))
        if white_score>black_score:
            winner = font.render ('Winner is white', 1, black)
            screen.blit (winner, (200,700))
    #remembering the winner's score in a file
    if game==False:                         #checking if the game is finished
        if white_score<black_score:         #assinging the winner's score to the variable
            winner_score = black_score
        else:
            winner_score = white_score
        


    return game


def rememberingScores(winner_score):        #function in which the top scores will be read into a list, the top score will be added, than
                                            #sorted descendingly and at the end written into a file
    top_scores=readingScores()              #calling a function that will read the top scores from a file
    #adding the next best score into the top_scores list
    if len (top_scores)<10:                 #if there are less than top 10 scores the new score is added automatically
        top_scores.append (winner_score)
    if len (top_scores)>10:                 #if there are already 10 scores
        if winner_score>top_scores[9]:      #it checks if the new score is bigger than the 10th score in the list
            top_scores[9] = winner_score    #if it is bigger it will be placed on the 10th place instead
        
    top_scores=sortingScores (top_scores)   #calling a function that will sort the top scores using bubble sort
    writingScores(top_scores)               #writes the updated best scores into a file


def sortingScores (top_scores):             #function that will sort decendingly the top scores using bubble sort
    for j in (top_scores):                  #it will run n times, where n is the number of the scores
        for i in range (0, len (top_scores)-1): #it will always take two adjacent numbers and compare them
            if top_scores [i]< top_scores [i+1]:#if they are not in correct order they will switch
                x=top_scores [i]
                top_scores [i] = top_scores [i+1]
                top_scores [i+1] = x
    return top_scores 

def readingScores():                            #function that will read the top scores from a file into a list
    top_scores=[]
    filename = 'BestScores.txt'
    file = open(filename, 'r')
    lines = file.readlines()
    for x in lines:
        top_scores.append (int(x.split()[1]))
    return top_scores

def writingScores(top_scores):                  #function that will write the top scores and their place into a file
    filename = 'BestScores.txt'
    file = open(filename, 'w')
    for i in range (0,len (top_scores)):
        file.write(str(i+1) + '.' + ' ')
        file.write(str(top_scores [i]) + '\n')




def startScore ():                                              #function that displays the start score on the screen (which is for both players 2)
    start_scoreW = font.render (str(2), 1, black)
    start_scoreB = font.render (str(2), 1, black)

    screen.blit (start_scoreW, (910,60))
    screen.blit (start_scoreB, (910,220))


titleWhite = fontTitle.render ('White Score', 1, black)     #writing heading of time, black and white score on the screen
titleBlack = fontTitle.render ('Black Score', 1, black)
time = fontTitle.render ('Time:', 1, black)

mousePosition = [0]*2


#functions that will validate user's moves
#all functions work on the same princip
def checkLeftUp(j,i, player, grid, valid_list): # function to check left up diagonal
#varibles passed into the function
#i,j are numbers of a clicked square
#player is color of current player
#grid is grid where stones are drawn
#valid_list is a list with true/false values that indicates if player made a valid move
#and whether the color of the player should be changed    
    change = False          #if change remains false no stones were reversed therefore the move is invalid
    if player == 'b':       #remembering the stone color that must be between two stones of the player's color
        colorCheck = 'w'
    else:
        colorCheck = 'b'

    if j>0 and i>0:         #check if the clicked square is not the left up corner if not the i,j value is decreased
        y=j-1               #by one and assign to x,y value to check if there are stones of the right color
        x=i-1
        while grid [y][x]==colorCheck and 0<y<=7 and 0<x<=7: #loop that follows the row of the same color stones and sets change
            x=x-1                                            #to true state if there is at least one stone of the other color
            y=y-1                                            #it also remembers x,y positon of the first square that doesnt have that color
            change = True
        if grid [y][x]==player and change ==True:           #if the move is valid the player's color is written into the grid and one zero
            grid [j][i]=player                              #in valid_list is changed into 1 so that at the end it can switch the players
            valid_list[7]=1 
            for k in range (1,(j-y+1)):                     #loop that changes the stones between two stones to the same color i
                grid[j-k][i-k]=player

def checkLeftDown(j,i, player, grid, valid_list):
    change = False
    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'

    if j<7 and i>0:
        y=j+1
        x=i-1
        while grid [y][x]==colorCheck and 0<=y<7 and 0<x<=7:
            x=x-1
            y=y+1
            change = True
        if grid [y][x]==player and change ==True:
            grid [j][i]=player
            valid_list[6]=1
            for k in range (1,(y-j+1)):
                grid[j+k][i-k]=player


def checkRightUp(j,i, player, grid, valid_list):
    change = False
    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'

    if j>0 and i <7:
        y=j-1
        x=i+1
        while grid [y][x]==colorCheck and 0<y<=7 and 0<=x<7:
            x=x+1
            y=y-1
            change = True
        if grid [y][x]==player and change ==True:
            grid [j][i]=player
            valid_list[5]=1
            for k in range (1,(j-y+1)):
                grid[j-k][i+k]=player


def checkRightDown(j,i, player, grid, valid_list):
    change = False
    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'
    if i<7 and j<7:
        y=j+1
        x=i+1
    
        while grid [y][x]==colorCheck and 0<=y<7 and 0<=x<7:
            x=x+1
            y=y+1
            change = True
        if grid [y][x]==player and change ==True:
            grid [j][i]=player
            valid_list[4]=1
            for k in range (1,(y-j+1)):
                grid[j+k][i+k]=player



def checkRight(j,i, player, grid, valid_list):
    change = False

    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'
    if i <7:
        y=j
        x=i+1
        while grid [y][x]==colorCheck and 0<=y<=7 and 0<=x<7:
            x=x+1
            change = True
        if grid [y][x]==player and change ==True:
            grid [j][i]=player
            valid_list[3]=1
            for k in range (i+1,x):
                grid[j][k]=player


def checkLeft(j,i, player, grid, valid_list):

    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'
    change = False
    
    if i>0:
        y=j
        x=i-1
        while grid [y][x]==colorCheck and 0<=y<=7 and 0<x<=7:
            x=x-1
            change = True
        if grid [y][x]==player and change ==True:
            grid [j][i]=player
            valid_list[2]=1
            for k in range (i-1,x,-1):
                grid[j][k]=player





#smer dolu 
def checkDown(j,i, player, grid, valid_list):

    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'
    change = False

    if j<7:
        y=j+1
        x=i
        while grid [y][x]==colorCheck and 0<=y<7 and 0<=x<=7:
            y=y+1
            change = True
        if grid [y][x]==player and change ==True:
            grid [j][i]=player
            valid_list[1]=1
            for k in range (j+1,y):
                grid[k][i]=player


#smer nahoru 
def checkUp(j,i, player, grid, valid_list):

    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'

    change = False
    
    if j>0:
        y=j-1
        x=i
        while grid [y][x]==colorCheck and 0<y<=7 and 0<=x<=7:
            y=y-1
            change = True
        if grid [y][x]==player and change ==True:
            grid [j][i]=player
            valid_list[0]=1
            for k in range (j-1,y,-1):
                grid[k][i]=player



def LeftUp(j,i, player, grid, valid_list): # function to check left up diagonal
    change = False          #if change remains false no stones were reversed therefore the move is invalid
    if player == 'b':       #remembering the stone color that must be between two stones of the player's color
        colorCheck = 'w'
    else:
        colorCheck = 'b'

    if j>0 and i>0 and grid [j][i]==player:         #check if the clicked square is not the left up corner if not the i,j value is decreased
        y=j-1               #by one and assign to x,y value to check if there are stones of the right color
        x=i-1
        while grid [y][x]==colorCheck and 0<y<=7 and 0<x<=7: #loop that follows the row of the same color stones and sets change
            x=x-1                                            #to true state if there is at least one stone of the other color
            y=y-1                                            #it also remembers x,y positon of the first square that doesnt have that color
            change = True
        if grid [y][x]==0 and change ==True:           #if the move is valid the player's color is written into the grid and one zero
            valid_list[7]=1 

def LeftDown(j,i, player, grid, valid_list):
    change = False
    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'

    if j<7 and i>0 and grid [j][i]==player:
        y=j+1
        x=i-1
        while grid [y][x]==colorCheck and 0<=y<7 and 0<x<=7:
            x=x-1
            y=y+1
            change = True
        if grid [y][x]==0 and change ==True:
            valid_list[6]=1
    

def RightUp(j,i, player, grid, valid_list):
    change = False
    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'

    if j>0 and i <7 and grid [j][i]==player:
        y=j-1
        x=i+1
        while grid [y][x]==colorCheck and 0<y<=7 and 0<=x<7:
            x=x+1
            y=y-1
            change = True
        if grid [y][x]==0 and change ==True:
            valid_list[5]=1


def RightDown(j,i, player, grid, valid_list):
    change = False
    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'
    if i<7 and j<7 and grid [j][i]==player:
        y=j+1
        x=i+1
    
        while grid [y][x]==colorCheck and 0<=y<7 and 0<=x<7:
            x=x+1
            y=y+1
            change = True
        if grid [y][x]==0 and change ==True:
            valid_list[4]=1



def Right(j,i, player, grid, valid_list):
    change = False

    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'
    if i <7 and grid [j][i]==player:
        y=j
        x=i+1
        while grid [y][x]==colorCheck and 0<=y<=7 and 0<=x<7:
            x=x+1
            change = True
        if grid [y][x]==0 and change ==True:
            valid_list[3]=1


def Left(j,i, player, grid, valid_list):

    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'
    change = False
    
    if i>0 and grid [j][i]==player:
        y=j
        x=i-1
        while grid [y][x]==colorCheck and 0<=y<=7 and 0<x<=7:
            x=x-1
            change = True
        if grid [y][x]==0 and change ==True:
            valid_list[2]=1



#smer dolu 
def Down(j,i, player, grid, valid_list):

    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'
    change = False

    if j<7 and grid [j][i]==player:
        y=j+1
        x=i
        while grid [y][x]==colorCheck and 0<=y<7 and 0<=x<=7:
            y=y+1
            change = True
        if grid [y][x]==0 and change ==True:
            valid_list[1]=1




#smer nahoru 
def Up(j,i, player, grid, valid_list):

    if player == 'b':
        colorCheck = 'w'
    else:
        colorCheck = 'b'
    change = False
    if j>0 and grid [j][i]==player:
        y=j-1
        x=i
        while grid [y][x]==colorCheck and 0<y<=7 and 0<=x<=7:
            y=y-1
            change = True
        if grid [y][x]==0 and change ==True:
            valid_list[0]=1





#-----------Main Program Loop-----------#
screen.fill (green)                                     #setting background colour
drawGrid ()                                             #draw a game board grid
drawStones(grid)                                        #drawing initial position of the game
startScore ()                                           #calling a function that displays start score
pygame.draw.circle(screen, black, (770,190), 20, 0)     #draw black circle next to Black Score heading to indicate that the starting player is black

screen.blit (titleWhite, (800,10))                      #Displaying titles for white & black score
screen.blit (titleBlack, (800,170))                     
screen.blit (time, (700,330))                           #Displaying title for game timer


while done == False:                                    #while loop that will run until cross on the window is pressed

    for event in pygame.event.get():                    #checks for an event (eg. mouse click)
        if event.type == pygame.QUIT:                   #if user clicked on cross on the windo the loop is terminated
            done = True

               
        if event.type == pygame.MOUSEMOTION:            #checks for mouse motion events
            mousePosition [:] = list(event.pos)
            hand1.moveHand (mousePosition)              #function that enables the hand cursor to move

        if event.type == pygame.MOUSEBUTTONUP:          #checks for clicks events
            #and event_handler function is called
            grid, player, frame_count, list_of_moves, no_of_moves,game = Button().event_handler(event, mousePosition,grid, player, frame_count, list_of_moves, no_of_moves,game)
            if game == True:
                    
                #if there is a click than move function is called
                player, grid, valid, list_of_moves, no_of_moves = move (grid, mousePosition, player, list_of_moves, no_of_moves)

                #drawStones function is called
                drawStones (grid)

                #score function is called
                white_score, black_score=score (grid)

                #winner function is called
                game=winner (white_score, black_score, grid,game)

        mouse = pygame.mouse.get_pos ()                 #for every event variable mouse holds position of the mouse
        
    
    #---Update Sprites---#


    #---Creating buttons---#
    pygame.draw.rect (screen, green, (740,490,400,300),0)   #draw a green rectangle over the buttons so that the mouse is not stacked on the screen
    scoreBut.drawRect (750,500)                             #drawing four rectagles that represent buttons
    new_gameBut.drawRect (1000,500)
    ruleBut.drawRect (750, 640)
    undoBut.drawRect (1000,640)
    
    Button().cursor(mousePosition)                          #calling a function that changes a mouse cursor into a hand cursor

    Button().heading('score')                               #entitling the four buttons
    Button().heading('new_game')
    Button().heading('help')
    Button().heading('undo')

    #---End of buttons---#
    

    # --- Timer ---#                                        #Calculate total minutes and seconds
    pygame.draw.rect (screen, green, (850,335,125,75), 0)   #draw green rectangle to have only one time visible

    total_seconds = frame_count // (frame_rate)             #calculate total 'updates of the screen' and divides it with frame rate
    minutes = total_seconds // 60                           #to get minutes we divide total_seconds by 60
    seconds = total_seconds % 60                            #second are the rest after division by 60
  
    output_string = "{0:02}:{1:02}".format(minutes, seconds)#python string formatting to format in leading zeros
 
    text = font.render(output_string, True, black)          #display time on the screen
    screen.blit(text, [850, 335])
    frame_count += 1
    #---End of Timer---#

    clock.tick(frame_rate)                                  #sets speed of the update to 20 frames/second
    pygame.display.flip()                                   #updates screen

pygame.quit ()                                              #closes the game window

    
