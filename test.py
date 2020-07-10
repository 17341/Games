self.add_txt("Score : ",0,5,COLORS["WHITE"],size = 30)
        self.add_txt("  Player°1 :",0,30,COLORS["RED"],size = 30)
        self.add_txt("  Player°2 :",0,55,COLORS["YELLOW"],size = 30)   
self.add_txt("Possible Moves : ",0,80,COLORS["WHITE"],size = 30)
        self.add_txt(str(n),10,110,COLORS["BLUE"],size = 30)
if n != 0 :
            if self.player1 > self.player2 :
                self.add_txt("Player°1 is winning!",335,520,COLORS["RED"],size = 30)
            if self.player1 < self.player2 : 
                self.add_txt("Player°2 is winning !",335,520,COLORS["YELLOW"],size = 30)
        self.add_txt("Status : ",250,520,COLORS["WHITE"],size = 30)
class Avalam_AI :
    
    def tac_five(self):
        self.five = {}   
        for f in game.coup_possible.keys():   
            self.five[f] = []
            for pos in game.coup_possible[f]:  
                if len(game.body["game"][f[0]][f[1]]) + len(game.body["game"][pos[0]][pos[1]]) == 5 : 
                    if game.body["game"][f[0]][f[1]][-1] == self.moi and game.body["game"][pos[0]][pos[1]][-1] != self.moi  : 
                        self.five[f].append(pos)                                                                              
        return(self.five) 
    def tac_isolate(self):
        self.isolate = {}
        for f in game.coup_possible.keys():
            self.isolate[f] = []
            if game.body["game"][f[0]][f[1]][-1] != self.moi: 
                for pos in game.coup_possible[f]:             
                     if game.body["game"][pos[0]][pos[1]][-1] == self.moi: 
                        self.isolate[f].append(pos)           
        return(self.isolate)
  
    def tac_minpoint(self):
        self.minpoint = {}
        for f in game.coup_possible.keys():
            self.minpoint[f] = []
            if game.body["game"][f[0]][f[1]][-1] != self.moi:  
                for pos in game.coup_possible[f]:
                     if game.body["game"][pos[0]][pos[1]][-1] != self.moi:
                        if len(game.body["game"][f[0]][f[1]]) + len(game.body["game"][pos[0]][pos[1]]) != 5 : 
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
                print(self.f, self.t)
                break
            if len(self.five[f]) > 0:
                self.f = list(f)
                self.t = choice(self.five[f])
                print(self.f, self.t)
                break  
            if len(self.minpoint[f]) > 0:
                self.f = choice(game.coup_possible[f])
                self.t = list(f)
                print(self.f, self.t)
                break
            else:
                self.random = {}
                for f in game.coup_possible.keys():
                    if len(game.coup_possible[f]) > 0:
                        self.random[f] = game.coup_possible[f]
                self.msg = choice(msg)
                self.f = list(choice(list(self.random.keys())))
                self.t = choice(self.random[tuple(self.f)] )