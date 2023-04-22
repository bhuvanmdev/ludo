from os import system
from re import search
from random import randint
class Ludo:
    ini = {'y': 0, 'b': 13, 'r': 26, 'g': 39}
    inner = {'y':[45,51],'b':[6,12],'r':[19,25],'g':[32,38]}
    def __init__(self):
        self.board = ['' for _ in range(52)]
        self.pos = {x:[-1 for _ in range(4)] for x in ('r','b','y','g')}
        self.tri = {x:['' for _ in range(6)] for x in ('r','b','y','g')}
        self.mov = 0
        self.winner = None
        self.player_name = {}
        self.order = {}

    def print_board(self):
        l,w = self.board,self.tri
        print('Green-XXXX'.center(29)+(l[49].center(4,'*')+' | '+l[50].center(4,'*')+' | '+l[51].center(4,'*'))+'Yellow-XXXX'.center(29))
        [print((l[48-x].center(4,'*')+' | '+w['y'][x].center(4,'-')+' | '+l[x].center(4,'*')).rjust(47)) for x in range(5)]

        print('|'.join(list(map(lambda x:x.center(4,'*'),l[38:44])))+'|'+6*' '+w['y'][-1].center(4,'-')+6*' '+'|'+ '|'.join(list(map(lambda x:x.center(4,'*'),l[5:11]))))
        print(l[37].center(4,'*')+'|'+'|'.join(list(map(lambda x:x.center(4,'-'),w['g'])))+8*' '+'|'.join(list(map(lambda x:x.center(4,'-'),w['b'][::-1])))+'|'+l[11].center(4,'*'))
        print('|'.join(list(map(lambda x:x.center(4,'*'),l[36:30:-1])))+'|'+6*' '+w["r"][-1].center(4,'-')+6*' '+'|'+'|'.join(list(map(lambda x:x.center(4,'*'),l[17:11:-1]))))

        [print((l[30-x].center(4,'*')+' | '+w["r"][::-1][x+1].center(4,'-')+' | '+l[18+x].center(4,'*')).rjust(47)) for x in range(5)]
        print('Red-XXXX'.center(29)+(l[25].center(4,'*') + ' | ' + l[24].center(4,'*') + ' | ' + l[23].center(4,'*'))+'Blue-XXXX'.center(29))
        print('\n')

    def mover(self,name,to):
        color,num = name[0],int(name[1])
        real_pos = self.pos[color][num]
        real_to = (real_pos + to)%52

        if real_pos == -2 or self.inner[color][0] <= real_pos <= self.inner[color][1]:
            if real_pos == -2:
                return self.inserter(name, to)
            with_roll = self.inner[color][1] - real_pos - 1
            if with_roll < to:
                return self.mover(name,with_roll) and self.inserter(name,to-with_roll)



        passer = False if real_to in self.ini.values() else True # for allowing to pass in safe places

        if real_pos==-1: return False

        # checks middle places
        co = 'rbwy'.replace(color, '')
        for x in range(real_pos+1,real_to):
         ##search_match
            if search(f'(^[{co}][0-3][{co}][0-3]$)|(^[{co}][0-3]$)',self.board[x]) and x not in self.ini.values():
                return False

        cond2 = search(f'[{co}]', self.board[real_to]) and len(self.board[real_to])==2

        #checks if the board is empty or is there a opp... color pawn
        if self.board[real_to] == '' or cond2:
            if cond2 and passer:
                c, n = self.board[real_to]
                self.pos[c][int(n)] = -1
            original_str = self.board[real_pos]
            self.board[real_pos] = original_str.replace(name,'')
            self.board[real_to] = name if passer else self.board[real_to]+name
            self.pos[color][num] = real_to
            return True

        ##search_match
        elif search(f'^{color}[0-3]$',self.board[real_to]):
            self.board[real_pos] = self.board[real_pos].replace(name,'')
            self.board[real_to] += name
            self.pos[color][num] = real_to
            return True

        # checks if the board as same color pawns

        return False


    def inserter(self,name,to):
        c,n = name
        for num,x in enumerate(self.tri[c]):
            if n in x:
                if num+to <= 5:
                    self.tri[c][num+to] += n
                    self.tri[c][num] = self.tri[c][num].replace(n,'')
                    self.winner = c if len(self.tri[c][-1]) == 4 else None
                    return True
                else:
                    return False
        else:
            self.pos[c][int(n)] = -2
            self.board[self.inner[c][1]-1] = self.board[self.inner[c][1]-1].replace(name,'')
            self.tri[c][to-1] += n
            self.winner = c if len(self.tri[c][-1]) == 4 else None
            return True

    def setter(self,player_num):
        if type(player_num) != int or not(1<=player_num<=4):
            raise TypeError
        colors = ['red','green','blue','yellow']
        for x in range(player_num):
            while (color:=input(f'give the color of {x+1} player: ').lower()) not in colors:
                print('wrong colour given\navailable colours are',colors)
            while 3 < len(name:=input('give their name: ')) > 10:
                print('the name is quite big make sure its <=10 and >=3')
            self.player_name[color[0]] = name
            self.order[x] = color[0]
            colors.remove(color)
        return player_num

    def out_bringer(self,color):
        for x in range(4):
            if self.pos[color][x] == -1:
                self.pos[color][x] = self.ini[color]
                self.board[self.ini[color]] += color+str(x)
                return True
        return False


    def starter(self):
        tot_player = self.setter(int(input("total_players: ")))
        not_roll = 0
        while True:
            turn = self.order[self.mov%tot_player][0]
            roll,cou = (randint(1,6),0) if not_roll == 0 else (roll,cou)
            not_roll = 0
            system('cls')
            print('your roll is ', roll, turn)
            self.print_board()
            if roll in (1,6):
                while (choice:=input('you can either move a pawn(m) or bring one out(b): ').lower()) not in ('b','m'):
                    print('invalid input')
                if (choice=='b' and self.out_bringer(turn)) or (choice == 'm' and self.mover(turn+(input("name: ")),roll)):
                    system('cls')
                    self.print_board()

                    if roll == 1:
                        self.mov+=1
                else:
                    print('invalid move')
                    cou += 1
                    if cou == 3:
                        print('sorry i guess u have no moves')
                        break
                    not_roll = 1
            else:
                if self.pos[turn].count(-1) == 4:
                    print('better luck next time',turn)
                    input()
                else:
                    cou = 0
                    while True:
                        while (name:=input('give me the pawn: '))=='' or name[0] not in ('1','0','2','3'):
                            print('invalid')
                        if self.mover(turn+name,roll):
                            system('cls')
                            self.print_board()
                            break
                        else:
                            print(name,"can't be moved, try other pawns")
                            cou += 1
                            if cou == 3:
                                print('sorry i guess u have no moves')
                                break
                self.mov += 1

            if self.winner != None:
                print(f'congratulations colour {self.winner} played by {self.player_name[self.winner]} is the winner')
                break
