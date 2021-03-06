import pygame, Heli, time
from StartMenu import menüü
from Võiduekraan import võiduekraan

sw=640#ekraani suuruse muutuja
sh=480

map = [[[('player',80,400,(225,0,0)),('wall',0,0,20,480),('wall',0,0,640,20),('wall',0,460,640,20),('wall',620,140,20,400),('wall',480,140,200,50),('wall',480,280,280,60),('wall',300,0,80,200),('wall',200,300,80,300),('wall',346,391,70,100),('lose area',280,404,350,100)],[('wall',0,0,640,20),('wall',0,140,20,400),('wall',0,140,150,50),('wall',620,0,20,100),('wall',520,150,100,50),('wall',620,150,20,500),('wall',0,460,280,20),('wall',340,460,300,20),('wall',400,300,240,50),('lose area',0,400,280,60),('lose area',340,400,280,60)],[('wall',0,0,20,100),('wall',0,0,640,20),('wall',620,0,20,400),('wall',0,460,680,20),('wall',0,150,20,330),('wall',20,240,80,220),('wall',100,320,80,140),('wall',180,400,80,60),('drone',280,440,(0,255,0),((280,440,None),(580,440,None)))],[('wall',0,0,640,20),('wall',0,0,20,400),('wall',620,0,20,480),('wall',0,460,190,100),('wall',280,460,360,100),('wall',130,240,60,240),('wall',130,180,310,60),('lose area',280,420,120,40)]],
       [[],[('wall',0,0,20,480),('wall',0,0,280,20),('wall',340,0,280,20),('wall',0,460,640,60),('wall',480,280,140,60),('wall',620,280,20,200)],[('wall',0,0,640,20),('wall',0,280,20,200),('wall',0,460,640,20),('wall',620,400,20,80),('wall',620,0,20,340),('wall',150,0,60,320),('wall',440,160,60,380),('wall',350,100,150,60)],[('wall',0,460,640,20),('wall',620,0,20,480),('wall',0,0,20,340),('wall',0,400,20,80),('wall',0,0,190,20),('wall',280,0,360,20),('wall',340,360,60,120),('wall',410,320,60,160),('wall',480,400,60,100),('win area',410,260,60,60)]]
       ]# list, mis koosneb korrustest, mis on listid, mis koosnevad tubadest, mis koosnevad kõikidest seintest ja tegelastest kes seal ilmuvad

x=0#näitab mitmendas toas tekitakse
y=0#näitab mitmendal korrusel tekitakse

pygame.init()

menüü()
algus = time.time()

window = pygame.display.set_mode([sw,sh])# teeb akna
taust = pygame.image.load("taustakas.jpg") #tausta laadimine
seinad1 = pygame.image.load("levels/level1.png")    #seina laadimine
seinad2 = pygame.image.load("levels/level2.png")
seinad3 = pygame.image.load("levels/level3.png")
seinad4 = pygame.image.load("levels/level4.png")
seinad5 = pygame.image.load("levels/level5.png")
seinad6 = pygame.image.load("levels/level6.png")
seinad7 = pygame.image.load("levels/level7.png")
robot=[pygame.image.load("uusrobot.png"),pygame.image.load("uus_robot2.png")]#roboti laadimine
jooks=[pygame.image.load("mängija_jooks/jooks1.png"),pygame.image.load("mängija_jooks/jooks2.png"),pygame.image.load("mängija_jooks/jooks3.png"),pygame.image.load("mängija_jooks/jooks4.png"),pygame.image.load("mängija_jooks/jooks5.png"),pygame.image.load("mängija_jooks/jooks6.png"),pygame.image.load("mängija_jooks/jooks7.png"),pygame.image.load("mängija_jooks/jooks8.png"),pygame.image.load("mängija_jooks/jooks9.png"),pygame.image.load("mängija_jooks/jooks10.png"),pygame.image.load("mängija_jooks/jooks11.png"),pygame.image.load("mängija_jooks/jooks12.png"),pygame.image.load("mängija_jooks/jooks13.png")]
seis=pygame.image.load("seis.png")
ronimine=[pygame.image.load("ronimine/ronimine1.png"),pygame.image.load("ronimine/ronimine2.png"),pygame.image.load("ronimine/ronimine3.png"),pygame.image.load("ronimine/ronimine4.png")]
huppamine=pygame.image.load('huppamine.png')
kukkumine=pygame.image.load('kukkumine.png')

class Person:
    def __init__(self,x,y,colour,drone=False,route=None):
        self.x=x
        self.y=y
        self.colour=colour
        self.vx=0
        self.vy=0
        self.points_bol=[False,False,False,# 9 punkti ruudu peal mis on true kui see puudutab seina ja false kui ei puuduta
                         False,False,False,
                         False,False,False]
        self.move_bol=[False,False,False,False,False]# näitab mis klahve vajutatakse
        self.jump1=False# näitab kas on võimalik teha esimest hüpet
        self.jump2=False# näitab kas on võimalik teha teist hüpet
        self.jump_bol=True
        self.var=0
        self.drone=drone
        self.route=route
        self.route_var=0
        if self.drone==True:
            self.set_goal()
        self.r=0
        self.ro=0

    def draw(self):#joonistab tegelase
        if self.drone==True:#joonistab roboti
            if self.vx<0:
                window.blit(robot[self.r],(self.x-20,self.y-20))
            elif self.vx>0:
                window.blit(pygame.transform.flip(robot[self.r], True, False),(self.x-20,self.y-20))
            if self.r==0:
                self.r=1
            elif self.r==1:
                self.r=0
        else:#joonistab tegelase mis pole robot
            if self.ro>3:
                self.ro=0
            if self.points_bol[5]==True:
                 window.blit(ronimine[self.ro],(self.x-20,self.y-20))
            elif self.points_bol[3]==True:
                 window.blit(pygame.transform.flip(ronimine[self.ro], True, False),(self.x-20,self.y-20))
            elif self.vx == 0 and self.points_bol[7]==True:
                window.blit(seis,(self.x-20,self.y-20))
            elif self.vx>0 and self.points_bol[7]==True:
                window.blit(jooks[self.r],(self.x-20,self.y-20))
                self.r+=1
            elif self.vx<0 and self.points_bol[7]==True:
                window.blit(pygame.transform.flip(jooks[self.r], True, False),(self.x-20,self.y-20))
                self.r+=1
            elif self.vy<0 and self.vx>0:
                 window.blit(huppamine,(self.x-20,self.y-20))
            elif self.vy<0 and self.vx==0:
                 window.blit(huppamine,(self.x-20,self.y-20))
            elif self.vy<0 and self.vx<0:
                 window.blit(pygame.transform.flip(huppamine, True, False),(self.x-20,self.y-20))
            elif self.vy>0 and self.vx>0:
                 window.blit(kukkumine,(self.x-20,self.y-20))
            elif self.vy>0 and self.vx<0:
                 window.blit(pygame.transform.flip(kukkumine, True, False),(self.x-20,self.y-20))
            elif self.vy>0 and self.vx==0:
                 window.blit(kukkumine,(self.x-20,self.y-20))
            if self.r>12:
                self.r=0

    def update(self,walls):#vaaab kas tegelane puudutab midagi
        self.points_bol=[False,False,False,#nullib ära
                         False,False,False,
                         False,False,False]
        self.jump1=False
        for s in walls:#kontrollib ära
            if self.x in range(s.x, s.x+s.w) and self.y + 20 in range(s.y,s.y+s.h):
                self.points_bol[7]=True
                self.y =s.y-20
                self.vy = 0
                self.jump1=True
                self.jump2=True
            elif self.x+20 in range(s.x, s.x+s.w) and self.y in range(s.y,s.y+s.h):
                self.points_bol[5]=True
                self.x =s.x-20
                self.jump1=True
                self.jump2=True
            elif self.x-20 in range(s.x, s.x+s.w) and self.y in range(s.y,s.y+s.h):
                self.points_bol[3]=True
                self.x =s.x+s.w+19
                self.jump1=True
                self.jump2=True
            elif self.x in range(s.x, s.x+s.w) and self.y-20 in range(s.y,s.y+s.h):
                self.points_bol[1]=True
                self.y =s.y+s.h+20
            elif self.x+20 in range(s.x, s.x+s.w) and self.y+20 in range(s.y,s.y+s.h):
                self.points_bol[8]=True
                self.jump1=True
                self.jump2=True
            elif self.x-20 in range(s.x, s.x+s.w) and self.y+20 in range(s.y,s.y+s.h):
                self.points_bol[6]=True
                self.jump1=True
                self.jump2=True
            elif self.x+20 in range(s.x, s.x+s.w) and self.y-20 in range(s.y,s.y+s.h):
                self.points_bol[2]=True
            elif self.x-20 in range(s.x, s.x+s.w) and self.y-20 in range(s.y,s.y+s.h):
                self.points_bol[0]=True

    def move(self):#liigutab tegelast
        if self.points_bol[7] == True:#kui seisab millegi peal kiirus alla on null
            self.vy = 0
        elif self.points_bol[7] == False:#kui ei seisa millegi peal siis hakkab alla kiirendama
            self.vy +=1

        if (self.move_bol[3]==False and self.move_bol[1]==False) and (self.points_bol[3]==True or self.points_bol[5]==True):# kui seisab selja küljel siis ei kukku alla
            self.vy =0
        elif (self.points_bol[3]==True or self.points_bol[5]==True) and self.move_bol[3]==True:#saab mööda seina alla liikuda
            self.vy= 5
            self.ro+=1
        elif (self.points_bol[3]==True or self.points_bol[5]==True) and self.move_bol[1]==True:#saab mööda seina üles liikuda
            self.vy=-5
            self.ro+=1

        if self.move_bol[0]==True and self.move_bol[2]==True:#kui hoiab all nii vasakut ja paremat ei liigu mitte midagi
            self.vx =0
        elif self.move_bol[0]==True and self.points_bol[3] != True:#liigub vasakule
            self.vx=-5
        elif self.move_bol[2]==True and self.points_bol[5] != True:#liigub paremale
            self.vx= 5

        if (self.move_bol[1]==True or self.move_bol[4]==True) and self.jump1==True and not (self.points_bol[3]==True or self.points_bol[5]==True) and self.jump_bol==True:#saab seina
            self.vy =-10
            self.jump1=False
            self.jump_bol=False
        elif (self.move_bol[1]==True or self.move_bol[4]==True) and self.jump2==True and not (self.points_bol[3]==True or self.points_bol[5]==True) and self.jump_bol==True:
            self.vy =-10
            self.jump2=False
            self.jump_bol=False
            
        if self.points_bol[3]==True and self.move_bol[4]==True and self.jump_bol==True:#esimene hüppe
            self.vy=-10
            self.vx= 5
            self.jump1 =False
            self.jump_bol=False
        elif self.points_bol[5]==True and self.move_bol[4]==True and self.jump_bol==True:
            self.vy=-10
            self.vx=-5
            self.jump1 =False
            self.jump_bol=False

        if self.drone==False:#aeglustab ainult kui pole robot
            if self.move_bol[0]==False and self.move_bol[2]==False and self.points_bol[7]==True:#aeglustab kui on maa peal
                self.vx= int(self.vx * 0.75)
##            if self.move_bol[0]==False and self.move_bol[2]==False and self.points_bol[7]==False:#aeglustab kui on õhus
##                if self.vx >0:
##                    self.vx=int(self.vx * 0.99)
##                if self.vx <0:
##                    self.vx=int(self.vx * 0.99)
        elif self.drone==True:#kui on robot peatub otse kohe
            if self.move_bol[0]==False and self.move_bol[2]==False and self.points_bol[7]==True:
                self.vx=0

        if self.move_bol[1]==True:
            self.var=1
        elif self.move_bol[4]==True:
            self.var=2

        if self.var!=0:
            if self.jump_bol==False and self.move_bol[1]==False and self.var==1:
                self.jump_bol=True
                self.var=0
            if self.jump_bol==False and self.move_bol[4]==False and self.var==2:
                self.jump_bol=True
                self.var=0

        self.x+=self.vx# liigutab tegelast
        self.y+=self.vy

    def set_goal(self):#paneb valmis selle kuhu robo tahab minna
        try:self.goal =self.route[self.route_var]
        except IndexError:
            self.route_var=0
            self.set_goal()
        if self.goal[2] != None:
            self.t1 = time.time() + self.goal[2]

    def go(self):# robot vajutab vasakule, paremale, üles, alla
        if self.goal[0] != None and self.goal[1] != None:
            if self.goal[0] < self.x:
                self.move_bol[0] = True
                self.move_bol[2] = False
            if self.goal[0] > self.x:
                self.move_bol[0] = False
                self.move_bol[2] = True
            if self.goal[0] == self.x:
                self.move_bol[0] = False
                self.move_bol[2] = False
            if self.goal[1] < self.y:
                self.move_bol[1] = True
                self.move_bol[3] = False
            if self.goal[1] > self.y:
                self.move_bol[1] = False
                self.move_bol[3] = True
            if self.goal[y] == self.y:
                self.move_bol[1] = False
                self.move_bol[3] = False
            if self.goal[0]==self.x and self.goal[1]==self.y:
                self.route_var+=1
                self.set_goal()
        elif self.goal[2] != None:
            if self.t1 < time.time():
                self.route_var+=1
                self.set_goal()

class Wall:#seinte klass
    def __init__(self,x,y,w,h):#sulgudesse tuleb alg kordinaadid, laiuse ja kõrgus
        self.x=x
        self.y=y
        self.w=w
        self.h=h

    def draw(self):#joonistab seina
        pygame.draw.rect(window,[0,0,0], [self.x, self.y, self.w, self.h],0)

class WinArea:#ala milles seistas võidad
    def __init__(self,x,y,w,h):#sulgudesse tuleb alg kordinaadid, laiuse ja kõrgus
        self.x=x
        self.y=y
        self.w=w
        self.h=h

    def draw(self):#joonistab võidu ala
        pygame.draw.rect(window,(71,209,255),[self.x, self.y, self.w, self.h],0)

    def win(self,player):#kui on võidu alas siis võidab
        if player.x in range(self.x,self.x+self.w) and player.y in range(self.y,self.y+self.h):
             return True
        else: return False

class LoseArea:#ala milles seistas kaotad
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h

    def draw(self):#joonistab kaotus ala
        pygame.draw.rect(window,(100,0,0),[self.x, self.y, self.w, self.h],0)

    def lose(self,player):#kui on kaotus alas siis kaotab
        if player.x in range(self.x,self.x+self.w) and player.y in range(self.y,self.y+self.h):
            player.__init__(80,400,(225,0,0))
            global x
            x=0
            global y
            y=0
            Heli.gameover()
            time.sleep(0.5)
            Heli.taustamuusika(-1)
            global algus
            algus = time.time()
            return True
        else:return False

def set_room(name):#võttab selle mis on ruumis ja teevad need asjadeks ekraanil
    ls=[]
    if name == 'walls':
        for i in map[y][x]:
            if i[0] == 'wall':
                ls.append(Wall(i[1],i[2],i[3],i[4]))
        return ls
    elif name == 'player':
        for i in map[y][x]:
            if i[0] == 'player':
                return Person(i[1],i[2],i[3])
    elif name == 'areas':
        for i in map[y][x]:
            if i[0] == 'lose area':
                ls.append(LoseArea(i[1],i[2],i[3],i[4]))
            if i[0] == 'win area':
                ls.append(WinArea(i[1],i[2],i[3],i[4]))
        return ls
    elif name == 'drones':
        for i in map[y][x]:
            if i[0] == 'drone':
                ls.append(Person(i[1],i[2],i[3],True,i[4]))
        return ls

player=set_room('player')
people=set_room('drones')
people.append(player)

walls =set_room('walls')

areas =set_room('areas')

Heli.taustamuusika(-1)

on=True
while on:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            on = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w or e.key == pygame.K_UP:
                player.move_bol[1]=True
            if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                player.move_bol[0]=True
            if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                player.move_bol[2]=True
            if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                player.move_bol[3]=True
            if e.key == pygame.K_SPACE:
                player.move_bol[4]=True
            if e.key == pygame.K_r:# paneb tegelase algusesse
                x=0
                y=0
                walls =set_room('walls')
                areas =set_room('areas')
                people=set_room('drones')
                people.append(player)
                player.__init__(80,400,(225,0,0))
                algus = time.time()
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_w or e.key == pygame.K_UP:
                player.move_bol[1]=False
            if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                player.move_bol[0]=False
            if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                player.move_bol[2]=False
            if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                player.move_bol[3]=False
            if e.key == pygame.K_SPACE:
                player.move_bol[4]=False

    window.blit(taust, (0, 0))  #joonistab tausta

    win =False

    try:
        for i in areas:#kontrollib kas mängija on kaotamis alas
            if i.lose(player) == True:
                walls =set_room('walls')
                areas =set_room('areas')
                people=set_room('drones')
                people.append(player)
    except NameError:pass
    except AttributeError:pass

    for a in areas:#joonistab alad
        a.draw()
    for p in people:#teeb kõik mis isikud peavad tegema
        if p.drone==True:#teeb kõik mis on robit peab tegema
            p.go()
            if player.x in range(p.x-20,p.x+20) and player.y in range(p.y-20,p.y+20):
                x=0
                y=0
                Heli.gameover()
                time.sleep(0.5)
                Heli.taustamuusika(-1)
                people=set_room('drones')
                walls =set_room('walls')
                areas =set_room('areas')
                player.__init__(80,400,(225,0,0))
                people.append(player)
                algus = time.time()

        p.move()
        p.update(walls)
        p.draw()

    if player.x < 0:#liigutab mängia ühest ruumist teise
        x-=1
        player.x = sw
        walls =set_room('walls')
        areas =set_room('areas')
        people=set_room('drones')
        people.append(player)
    elif player.x>sw:
        x+=1
        player.x=0
        walls =set_room('walls')
        areas =set_room('areas')
        people=set_room('drones')
        people.append(player)
    if player.y<0:
        y-=1
        player.y=sh
        walls =set_room('walls')
        areas =set_room('areas')
        people=set_room('drones')
        people.append(player)
    elif player.y>sh:
        y+=1
        player.y=0
        walls =set_room('walls')
        areas =set_room('areas')
        people=set_room('drones')
        people.append(player)

    if x==0 and y==0:#joonistab ruumid olenevalt mis toas ollakse
        window.blit(seinad1, (0, 0))
    elif x==1 and y==0:
        window.blit(seinad2, (0, 0))
    elif x==2 and y==0:
        window.blit(seinad3, (0, 0))
    elif x==3 and y==0:
        window.blit(seinad4, (0, 0))
    elif x==3 and y==1:
        window.blit(seinad5, (0, 0))
    elif x==2 and y==1:
        window.blit(seinad6, (0, 0))
    elif x==1 and y==1:
        window.blit(seinad7, (0, 0))

    try:#kontrollib kas on võidu alas
        for i in areas:
            if i.win(player) == True:
                win=True
    except NameError:pass
    except AttributeError:pass

    if win == True:#kui on võidu alas teeb asju
        lõpp = time.time()
        print(lõpp)
        koguaeg = str(round(lõpp - algus, 2))+" s"
        print(koguaeg)
        võiduekraan(koguaeg)
        x=0
        y=0
        walls =set_room('walls')
        areas =set_room('areas')
        people=set_room('drones')
        player.__init__(80,400,(225,0,0))
        people.append(player)
        Heli.taustamuusika(-1)
        algus = time.time()

    pygame.display.flip()
    pygame.time.delay(17)
pygame.quit()
