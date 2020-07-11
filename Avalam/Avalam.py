import pygame
import pygame
from pygame.locals import *
import time 
from random import choice

pygame.init()


BOARD={"0":[6,7],
        "1":[4,5,6,7],
        "2":[2,3,4,5,6,7],
        "3":[0,1,2,3,4,5,6,7],
        "4":[0,1,2,3,4,5,6,7,8],
        "5":[1,2,3,4,5,6,7,8],
        "6":[1,2,3,4,5,6],
        "7":[1,2,3,4],
        "8":[1,2]}
CASE_WIDTH = 50
CASE_HEIGHT = 50
CASE_SPACE = 10
PAWN_RADIUS = 25
COLORS={"BLACK" : (0, 0, 0),
        "WHITE" : (255, 255, 255),
        "GREEN":(0, 255, 0),
        "RED" :(255, 0, 0),
        "YELLOW":(255,255,0),
        "BLUE":(0,0,255),
        "GRAY":(128,128,128)}
board_color = {}

chess_drop_sound = pygame.mixer.Sound("Avalam\Sounds\Chess_drop.wav")
chess_move_sound = pygame.mixer.Sound("Avalam\Sounds\Chess_move.wav")

class Avalam_Game:

    def __init__(self):
        self.moi = 0
        self.board_color = board_color
        self.BOARD=BOARD
        self.CASE_WIDTH = CASE_WIDTH
        self.CASE_HEIGHT = CASE_HEIGHT 
        self.CASE_SPACE = CASE_SPACE
        self.PAWN_RADIUS = PAWN_RADIUS
        self.GRID = [[0 for x in range(9)] for y in range(9)]
        self.WINDOW_SIZE = [self.CASE_HEIGHT*len(self.GRID)+(self.CASE_SPACE*(len(self.GRID)+1)),len(self.GRID)*self.CASE_WIDTH+(self.CASE_SPACE*(len(self.GRID)+1))]
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        self.moves = {}
        self.body = [[[] for x in range(9)]for y in range(9)]
        self.joueur = 0
        for row in self.BOARD.keys() :
            for column in self.BOARD[row]: 
                if int(row) % 2 != 0 and int(column) % 2 == 0 or int(row) % 2 == 0 and int(column) % 2 != 0:
                    self.body[int(row)][int(column)] =  [1]
                    self.board_color[(int(row),column)] = ["RED"]
                else:
                    self.body[int(row)][int(column)] = [0]
                    self.board_color[(int(row),column)] = ["YELLOW"]
        self.moves_messages = [" "]
        self.problem_messages = [" "]
                
    def draw_board(self):
        self.possible_moves()
        self.screen.fill(COLORS["BLACK"])
        pygame.display.set_caption("Avalam")
        for pos in self.board_color.keys():
            row_pos =  int(pos[0])*(self.CASE_HEIGHT + self.CASE_SPACE)
            col_pos =  int(pos[1])*(self.CASE_WIDTH + self.CASE_SPACE)
            pygame.draw.circle(self.screen,COLORS[self.board_color[pos][-1]],(col_pos+(int(self.PAWN_RADIUS+self.CASE_SPACE)),row_pos+(int(self.PAWN_RADIUS+self.CASE_SPACE))), int(self.PAWN_RADIUS), int(self.PAWN_RADIUS))
            num = len(self.body[pos[0]][pos[1]])
            self.add_txt(num,col_pos+self.PAWN_RADIUS,row_pos+self.PAWN_RADIUS-5,COLORS["BLUE"])
                    
        return(self.BOARD)

    def pawn_position(self):
        self.position = []
        self.coup_possible = {}    
        for l in range(9):              
            for c in range(9):          
                if len(self.body[l][c]) < 5 and len(self.body[l][c]) != 0:
                    self.position.append([l,c])
                    self.coup_possible[l,c] = []
        return(self.position)

    def possible_moves(self): 
        self.pawn_position()
        for f in self.position:      
            l = f[0]                 
            c = f[1]           
            if c < 8 and len(self.body[l][c+1]) < 5 and len(self.body[l][c+1]) != 0 : 
                if (len(self.body[l][c]) + len(self.body[l][c+1])) <= 5 : 
                    self.coup_possible[l,c].append([l,c+1])
            if c > 0 and len(self.body[l][c-1]) < 5 and len(self.body[l][c-1]) != 0 : 
                if (len(self.body[l][c]) + len(self.body[l][c-1])) <= 5 :     
                    self.coup_possible[l,c].append([l,c-1])
            if l < 8 and len(self.body[l+1][c]) < 5 and len(self.body[l+1][c]) != 0 : 
                if (len(self.body[l][c]) + len(self.body[l+1][c])) <= 5 :     
                    self.coup_possible[l,c].append([l+1,c])
            if l > 0 and len(self.body[l-1][c]) < 5 and len(self.body[l-1][c]) != 0 : 
                if (len(self.body[l][c]) + len(self.body[l-1][c])) <= 5 :     
                    self.coup_possible[l,c].append([l-1,c])
            if l > 0  and c > 0 and len(self.body[l-1][c-1]) < 5 and len(self.body[l-1][c-1]) != 0 : 
                if (len(self.body[l][c]) + len(self.body[l-1][c-1])) <= 5 :     
                    self.coup_possible[l,c].append([l-1,c-1])
            if l > 0 and c < 8 and len(self.body[l-1][c+1]) < 5 and len(self.body[l-1][c+1]) != 0 : 
                if (len(self.body[l][c]) + len(self.body[l-1][c+1])) <= 5 :     
                    self.coup_possible[l,c].append([l-1,c+1])
            if l < 8 and c > 0  and len(self.body[l+1][c-1]) < 5 and len(self.body[l+1][c-1]) != 0 : 
                if (len(self.body[l][c]) + len(self.body[l+1][c-1])) <= 5 :     
                    self.coup_possible[l,c].append([l+1,c-1])   
            if l < 8 and c < 8 and len(self.body[l+1][c+1]) < 5 and len(self.body[l+1][c+1]) != 0 : 
                if (len(self.body[l][c]) + len(self.body[l+1][c+1])) <= 5 :     
                    self.coup_possible[l,c].append([l+1,c+1])
        return(self.coup_possible)

    def show_move(self,position):
        try :
            for possible in self.coup_possible[position]:
                pos2 =  int(possible[0])*(self.CASE_HEIGHT + self.CASE_SPACE)
                pos1 =  int(possible[1])*(self.CASE_WIDTH + self.CASE_SPACE) 
                pygame.draw.circle(self.screen,COLORS["WHITE"],(pos1+(int(self.PAWN_RADIUS+self.CASE_SPACE)),pos2+(int(self.PAWN_RADIUS+self.CASE_SPACE))),int(self.PAWN_RADIUS),int(self.PAWN_RADIUS))
        except:
            game.problem_messages.append("Not possible :/ ")
            
    def make_move(self,initial_position,final_position):
        chess_move_sound.play()
        try : 
            if list(final_position) in self.coup_possible[initial_position] : 
                self.body[final_position[0]][final_position[1]] += self.body[initial_position[0]][initial_position[1]]
                self.body[initial_position[0]][initial_position[1]].clear()
                #Remove pawn from board : 
                for value in self.BOARD[str(initial_position[0])]:
                    if value == initial_position[1] :
                        self.BOARD[str(initial_position[0])].remove(value)
                #Remove color from pawn :
                for value in self.board_color.keys():
                    if  initial_position == value :
                        initial_color = self.board_color[value]
                        self.board_color[final_position] = initial_color
                        del self.board_color[value]
                        game.moves_messages.append("From {} To {}".format(initial_position,final_position))
                        break
                
            else:
                game.problem_messages.append("Not possible :/ ")  
                 
        except: 
            game.problem_messages.append("Not possible :/ ")
        self.joueur +=1 
               
        pygame.display.update()
   
    def add_txt(self,txt,x,y,color,size = 50):
        
        Letter_font = pygame.font.SysFont('comicsans',size)
        text = Letter_font.render(str(txt),1,color)
        self.screen.blit(text,(x,y))
        pygame.display.update()  

    def add_image(self,image,x,y):
        
        img= pygame.image.load(image) 
        self.screen.blit(img,(x,y))
        pygame.display.update()  
    
    def end(self):
        self.possible_moves()
        n = 0
        for elem in self.coup_possible.values() :
            n +=len(elem)
        
        if n == 0 :
            if self.player1 > self.player2 :
                self.add_txt("Player1 WON !",400,520,COLORS["BLUE"],size = 30)
            if self.player1 < self.player2 : 
                self.add_txt("Player2 WON !",400,520,COLORS["BLUE"],size = 30)
            time.sleep(5)
            quit()
        
    def score(self):
        self.player1 = 0
        self.player2 = 0
        for elem in self.body:
            for i in elem:
                try :
                    if i[-1] == 0 :
                        self.player2 += 1
                    else :
                        self.player1 += 1
                except:
                    pass

        self.add_txt(" Score : ",0,5,COLORS["WHITE"],size = 30)
        self.add_txt("   Player°1 : {}".format(self.player1),0,30,COLORS["RED"],size = 30)
        self.add_txt("   Player°2 : {}".format(self.player2),0,55,COLORS["YELLOW"],size = 30)

    def menu(self):
        pygame.display.set_caption("Avalam Menu")
        self.screen.fill(COLORS["GRAY"])
        pygame.draw.rect(self.screen,COLORS["YELLOW"], (10,150,530,100))
        pygame.draw.rect(self.screen,COLORS["GREEN"], (10,270,530,100))
        pygame.draw.rect(self.screen,COLORS["RED"], (10,390,530,100))

        pygame.draw.rect(self.screen,COLORS["RED"], (490,5,50,45))
        self.add_txt("S",500,10,COLORS["BLACK"],size = 60)

        self.add_txt("Main Menu ",165,50,COLORS["BLACK"],size = 60)
        self.add_txt("Play",220,180,COLORS["BLACK"],size = 60)
        self.add_txt("Info",220,300,COLORS["BLACK"],size = 60)
        self.add_txt("Quit",220,420,COLORS["BLACK"],size = 60)
        pygame.display.flip()    

    def status(self):
        pass
    """
        self.add_txt("Last Move :",220,520,COLORS["WHITE"],size = 30)
        self.add_txt(self.moves_messages[-1],340,520,COLORS["GREEN"],size = 30)
        self.add_txt("Last Problem : ",220,490,COLORS["WHITE"],size = 30)
        self.add_txt(self.problem_messages[-1],370,490,COLORS["GREEN"],size = 30)
    """    



class Avalam_AI :

    def move(self):
        self.IA()
        return(self.f, self.t)
    
    def tac_five(self):
        self.five = {}   
        for f in game.coup_possible.keys():   
            self.five[f] = []
            for pos in game.coup_possible[f]:  
                if len(game.body[f[0]][f[1]]) + len(game.body[pos[0]][pos[1]]) == 5 : 
                    if game.body[f[0]][f[1]][-1] == game.moi and game.body[pos[0]][pos[1]][-1] != game.moi  : 
                        self.five[f].append(pos)                                                                              
        return(self.five) 
    def tac_isolate(self):
        self.isolate = {}
        for f in game.coup_possible.keys():
            self.isolate[f] = []
            if game.body[f[0]][f[1]][-1] != game.moi: 
                for pos in game.coup_possible[f]:             
                     if game.body[pos[0]][pos[1]][-1] == game.moi: 
                        self.isolate[f].append(pos)           
        return(self.isolate)
  
    def tac_minpoint(self):
        self.minpoint = {}
        for f in game.coup_possible.keys():
            self.minpoint[f] = []
            if game.body[f[0]][f[1]][-1] != game.moi:  
                for pos in game.coup_possible[f]:
                     if game.body[pos[0]][pos[1]][-1] != game.moi:
                        if len(game.body[f[0]][f[1]]) + len(game.body[pos[0]][pos[1]]) != 5 : 
                            self.minpoint[f].append(pos) 
        return(self.minpoint)   

    def IA(self):
        self.tac_isolate()
        self.tac_five()
        self.tac_minpoint()
        for f in game.coup_possible.keys():
            if len(self.isolate[f]) == len(game.coup_possible[f]) and len(game.coup_possible[f]) > 0:
                self.f = choice(game.coup_possible[f]) 
                self.t = list(f) 
                
                break
            if len(self.five[f]) > 0:
                self.f = list(f)
                self.t = choice(self.five[f])
                
                break  
            if len(self.minpoint[f]) > 0:
                self.f = choice(game.coup_possible[f])
                self.t = list(f)
                
                break
            else:
                self.random = {}
                for f in game.coup_possible.keys():
                    if len(game.coup_possible[f]) > 0:
                        self.random[f] = game.coup_possible[f]
                self.f = list(choice(list(self.random.keys())))
                self.t = choice(self.random[tuple(self.f)] )

game = Avalam_Game()
ia = Avalam_AI()

def info():
    pygame.display.set_caption("Avalam Info")
    game.screen.fill(COLORS["GRAY"])
    game.add_txt("To add ... ",165,50,COLORS["BLACK"],size = 60)
    pygame.display.flip()   

def menu():
    music = 0 
    pygame.mixer.music.load("Avalam\Sounds\Menu.wav")
    pygame.mixer.music.set_volume(0.03)
    pygame.mixer.music.play(-1)
    game.menu()
    run = True
    play_rect = [(x, y ) for x in range(10,540) for y in range (150,250)]
    info_rect = [(x, y ) for x in range(10,540) for y in range (270,370)]
    quit_rect = [(x, y ) for x in range(10,540) for y in range (390,490)]
    music_button = [(x, y ) for x in range(490,540) for y in range (5,50)]
    while run :
        if music %2 == 0 :
            pygame.mixer.music.unpause() 
        mouse_pos = pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pos in music_button:
                pygame.mixer.music.pause()
                music += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pos in  play_rect :
                main()
            elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pos in info_rect :
                info()
            elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pos in  quit_rect : 
                quit()
                    
def main():
    run = True
    clock = pygame.time.Clock()
    FPS = 60
    show = 0
    game.screen.fill(COLORS["BLACK"])
    game.score()
    chess_drop_sound.play()
    time.sleep(0.4)
    game.draw_board()
    game.score()
    while run :
        ia.move()
        game.status()
        clock.tick(FPS)
        if int(game.joueur) %2== 0 : 
            while show%2 != 0 :
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  
                        quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        final_position = pygame.mouse.get_pos()
                        final_column = final_position[0] // (CASE_WIDTH + CASE_SPACE)
                        final_row = final_position[1] // (CASE_HEIGHT + CASE_SPACE)
                        
                        if [final_row,final_column] in game.coup_possible[(initial_row,initial_column)]:
                            game.make_move((initial_row,initial_column),(final_row, final_column))
                            game.draw_board()
                            game.score()
                            game.end()
                            show += 1 

                        elif(initial_row,initial_column) == (final_row,final_column) :
                            print("Pas possible")
                            game.draw_board()
                            game.score()
                            show -=1
                            
                        else :
                            print("Retry")
                            game.draw_board()
                            game.score()
                            show -=1     
                           
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  
                    quit()  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    initial_position = pygame.mouse.get_pos()
                    initial_column = initial_position[0] // (CASE_WIDTH + CASE_SPACE)
                    initial_row =initial_position[1] // (CASE_HEIGHT + CASE_SPACE)
                    if (len(game.body[initial_row][initial_column]) == 5) : 
                        print("Remplie")
                        break
                    elif str(initial_row) in BOARD.keys() and initial_column in BOARD[str(initial_row)]:
                        game.show_move((initial_row,initial_column))
                        show += 1
                    else :
                        game.problem_messages.append("No pawn here !")
                        print("No pawn here !")
                        
        else :
            ia.move()
            initial_position = ia.f
            final_position = ia.t
            time.sleep(1)
            game.make_move(tuple(initial_position),tuple(final_position))
            game.draw_board() 
            game.score()
            game.end()         
        pygame.display.flip() 

if __name__ == "__main__":
    menu()
 
