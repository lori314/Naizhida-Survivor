import pygame
import sys
import random
import math

SCREEN_WIDTH=1700
SCREEN_HEIGHT=900

class player(pygame.sprite.Sprite):
    def __init__(self,name) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.name=name
        if self.name=='zang':
            image=pygame.image.load(r'img\zang1.png')
            aim_image=pygame.image.load(r'img\aim.png')
            self.image=pygame.transform.scale(image,(75,75))
            is_shot_img=pygame.image.load(r'img\zang3.png')
            self.rect=self.image.get_rect()
            self.aim_image=pygame.transform.scale(aim_image,(30,30))
            self.aim_image_rect=self.aim_image.get_rect()
            self.aim_image_rect.topleft=(0,0)
            self.attack_image=pygame.transform.scale(pygame.image.load(r'img\circle.png'),(250,250))
            self.attack_image_rect=self.attack_image.get_rect()
            self.attack_image_rect.topleft=(0,0)
            self.is_shot_image=pygame.transform.scale(is_shot_img,(75,75))
            self.rect.topleft=(100,SCREEN_HEIGHT-90)
            self.speed=10
            self.blood=100
            self.live=True
            self.fight=False
            self.crazy=False
            self.has_crazy=True
            self.shot=False
            self.count=0
            self.wait=1000
            self.shot_count=0
            self.bombs=pygame.sprite.Group()
            self.bullets=pygame.sprite.Group()

    def move(self):
        if self.wait>=1500:
            self.has_crazy=True
        else:
            self.wait+=1
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_w]==1:
            self.rect.y-=self.speed
        if key_pressed[pygame.K_s]==1:
            self.rect.y+=self.speed
        if key_pressed[pygame.K_a]==1:
            self.rect.x-=self.speed
        if key_pressed[pygame.K_d]==1:
            self.rect.x+=self.speed
        if key_pressed[pygame.K_SPACE]==1 and self.crazy==False and self.has_crazy==True:
            self.crazy=True
            self.has_crazy=False
            self.wait=0
            self.count=0

    def attack(self):
        global enemy_list
        self.count+=1
        if self.count>=10000:
            self.count=0
        pos=pygame.mouse.get_pos()
        self.aim_image_rect.topleft=(pos[0]-15,pos[1]-15)
        mouse_pressed=pygame.mouse.get_pressed()
        if self.crazy==False:
            if mouse_pressed[0]==1 and self.count%4==0:
                pos=pygame.mouse.get_pos()
                m_bullet=bullet('zang',self.rect,pos)
                self.bullets.add(m_bullet)
            if mouse_pressed[2]==1:
                if self.fight==False and self.count>=50:
                    self.fight=True
                    self.count=0
        
        else:
            self.fight=True
            if mouse_pressed[0]==1 and self.count%2==0:
                pos=pygame.mouse.get_pos()
                bomb=Bomb('zang',pos)
                self.bombs.add(bomb)
            for bomb in self.bombs:
                bomb.display()
                enemies=pygame.sprite.spritecollide(bomb,enemy_list,False)
                for enemy in enemies:
                    enemy.blood-=bomb.hong
                bomb.count+=1
                if bomb.count>=10:
                    self.bombs.remove(bomb)
            if self.count>=500:
                self.crazy=False

        if self.fight==True:
            self.attack_image_rect.topleft=(self.rect.x-85,self.rect.y-85)
            scr.blit(self.attack_image,self.attack_image_rect)
            for enemy in enemy_list:
                if self.attack_image_rect.colliderect(enemy.rect):
                    d_x=self.rect.x-enemy.rect.x
                    d_y=self.rect.y-enemy.rect.y
                    enemy.rect.x-=int(200*(d_x)/((d_x**2+d_y**2)**0.5))
                    enemy.rect.y-=int(200*(d_y)/((d_x**2+d_y**2)**0.5))
                    enemy.blood-=8
                    if self.crazy==False:
                        self.blood+=3
                for bul in enemy.bullets:
                    if self.attack_image_rect.colliderect(bul.rect):
                        enemy.bullets.remove(bul)
            self.fight=False

        for m_bullet in self.bullets:
            m_bullet.auto_move()
            m_bullet.display()

    def is_shot(self):
        global enemy_list
        self.shot_count+=1
        if self.shot_count>=10000:
            self.shot_count=0
        if self.shot==True and self.shot_count%3==0:
            self.shot=False
        enemies= pygame.sprite.spritecollide(self,enemy_list,True)
        for enemy in enemies:
            self.blood-=enemy.blood
            enemy.blood=0
            self.shot=True
            self.shot_count=0
        for enemy in enemy_list:
            bullets=pygame.sprite.spritecollide(self,enemy.bullets,True)
            for bullet in bullets:
                if bullet.type=='goat':
                    self.blood-=1
                elif bullet.type=='star':
                    self.blood-=5
                enemy.bullets.remove(bullet)
                self.shot=True
                self.shot_count=0
                
        if self.blood<=0:
            self.live=False

    def display(self):
        if self.shot==True:
            scr.blit(self.is_shot_image,self.rect)
        else:
            scr.blit(self.image,self.rect)
        scr.blit(self.aim_image,self.aim_image_rect)

      

class goat(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        image=pygame.image.load(r'img\normal_enemy_goat1.png')
        self.image=pygame.transform.scale(image,(35,90))
        self.speed=2
        self.blood=20
        self.rect=self.image.get_rect()
        self.bullets=pygame.sprite.Group()
        p=random.randint(1,2)
        if p==1:
            self.rect.topleft=(random.randint(0,1500),0)
        else:
            self.rect.topleft=(1500,random.randint(0,SCREEN_HEIGHT))
        self.live=True
        self.crazy=False
        self.count=0
        self.score=5
    
    def auto_move(self,target):
        if self.rect.y<target.rect.y:
            self.rect.y+=self.speed
        elif self.rect.y>target.rect.y:
            self.rect.y-=self.speed
        if self.rect.x<target.rect.x+30:
            self.rect.x+=self.speed
        elif self.rect.x>target.rect.x+30:
            self.rect.x-=self.speed
    
    def shoot(self,target):
        self.count+=1
        if self.count>=10000:
            self.count=0
        if self.count%50==0:
            m_bullet=bullet('goat',self.rect,target)
            self.bullets.add(m_bullet)
        for m_bullet in self.bullets:
            m_bullet.auto_move()
            m_bullet.display()

    def display(self):
        scr.blit(self.image,self.rect)

    def is_shot(self,player_bullets):
        if pygame.sprite.spritecollide(self,player_bullets,True)!=[]:
            self.blood-=1
        if self.blood<=10 and self.crazy==False:
            self.crazy=True
            image=pygame.image.load(r'img\enemy_goat.png')
            self.image=pygame.transform.scale(image,(35,90))
            self.speed=8
        if self.blood<=0:
            self.live=False
    



class watermelon(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        image=pygame.image.load(r'img\enemy_watermelon.png')
        self.image=pygame.transform.scale(image,(50,50))
        self.speed=1
        self.super_speed=10
        self.count=0
        self.blood=10
        self.crazy=False
        self.move_way=[0,0,0,0]
        self.bullets=pygame.sprite.Group()
        self.rect=self.image.get_rect()
        self.live=True
        p=random.randint(1,2)
        if p==1:
            self.rect.topleft=(random.randint(0,1500),0)
        else:
            self.rect.topleft=(1500,random.randint(0,SCREEN_HEIGHT))
        self.score=5
    def auto_move(self,target):
        self.count+=1
        if self.count>=100:
            self.count=0
        if self.count>=60:
            if self.crazy==False:
                if self.rect.y<target.rect.y:
                    self.move_way[0]=1
                    self.move_way[1]=0
                elif self.rect.y>target.rect.y:
                    self.move_way[0]=0
                    self.move_way[1]=1
                if self.rect.x<target.rect.x+30:
                    self.move_way[2]=1
                    self.move_way[3]=0
                elif self.rect.x>target.rect.x+30:
                    self.move_way[2]=0
                    self.move_way[3]=1
                self.crazy=True
            if self.crazy==True:
                if self.move_way[0]:
                    self.rect.y+=self.super_speed
                elif self.move_way[1]:
                    self.rect.y-=self.super_speed
                if self.move_way[2]:
                    self.rect.x+=self.super_speed
                elif self.move_way[3]:
                    self.rect.x-=self.super_speed

        else:
            self.crazy=False
            if self.rect.y<target.rect.y:
                self.rect.y+=self.speed
            elif self.rect.y>target.rect.y:
                self.rect.y-=self.speed
            if self.rect.x<target.rect.x+30:
                self.rect.x+=self.speed
            elif self.rect.x>target.rect.x+30:
                self.rect.x-=self.speed

    def is_shot(self,player_bullets):
        if pygame.sprite.spritecollide(self,player_bullets,True)!=[]:
            self.blood-=1
        if self.blood<=0:
            self.live=False

    def display(self):
        scr.blit(self.image,self.rect)

class star(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        image=pygame.image.load(r'img\star0.png')
        self.image=pygame.transform.scale(image,(100,100))
        self.rect=self.image.get_rect()
        p=random.randint(1,2)
        if p==1:
            self.rect.topleft=(random.randint(0,1500),0)
        else:
            self.rect.topleft=(1500,random.randint(0,SCREEN_HEIGHT))
        self.speed=2
        self.blood=50
        self.bullets=pygame.sprite.Group()
        self.count=0
        self.live=True
        self.score=20
    
    def auto_move(self,target):
        if self.rect.y<target.rect.y:
            self.rect.y+=self.speed
        elif self.rect.y>target.rect.y:
            self.rect.y-=self.speed
        if self.rect.x<target.rect.x+30:
            self.rect.x+=self.speed
        elif self.rect.x>target.rect.x+30:
            self.rect.x-=self.speed
    
    def shoot(self,target):
        self.count+=1
        if self.count>=10000:
            self.count=0
        if self.count%(120+random.randint(-10,10))==0:
            for order in range(0,5):
                m_bullet=bullet('star',self.rect,target,order)
                self.bullets.add(m_bullet)
        for m_bullet in self.bullets:
            m_bullet.auto_move()
            m_bullet.display()

    def is_shot(self,player_bullets):
        if pygame.sprite.spritecollide(self,player_bullets,True)!=[]:
            self.blood-=1
        if self.blood<=0:
            self.live=False

    def display(self):
        scr.blit(self.image,self.rect)


class bullet(pygame.sprite.Sprite):
    def __init__(self,type,rect,target,order=0) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.type=type
        if self.type=='goat':
            image=pygame.image.load(r'img\enemy_bullet.png')
            self.image=pygame.transform.scale(image,(12,12))
            self.rect=self.image.get_rect()
            self.rect.topleft=(rect.x+17-12/2,rect.y+45-12/2)
            self.speed=5
            self.x=target.rect.x-rect.x
            self.y=target.rect.y-rect.y
            self.speed_x=int(self.speed*(self.x)/((self.x**2+self.y**2)**0.5))
            self.speed_y=int(self.speed*(self.y)/((self.x**2+self.y**2)**0.5))
        
        if self.type=='star':
            image=pygame.image.load(r'img\star_bullet.png')
            self.image=pygame.transform.scale(image,(24,24))
            self.rect=self.image.get_rect()
            self.rect.topleft=(rect.x+50-24/2,rect.y+50-24/2)
            self.speed=8
            self.speed_x=int(self.speed*math.sin(order*72))
            self.speed_y=int(self.speed*math.cos(order*72))
        
        if self.type=='zang':
            image=pygame.image.load(r'img\zang_bullet.png')
            self.image=pygame.transform.scale(image,(18,18))
            self.rect=self.image.get_rect()
            self.rect.topleft=(rect.x+37-18/2,rect.y+37-18/2)
            self.speed=50
            self.x=target[0]-rect.x
            self.y=target[1]-rect.y
            self.speed_x=int(self.speed*(self.x)/((self.x**2+self.y**2)**0.5))
            self.speed_y=int(self.speed*(self.y)/((self.x**2+self.y**2)**0.5))

    def auto_move(self):
        self.rect.x+=self.speed_x
        self.rect.y+=self.speed_y

    def display(self):
        scr.blit(self.image,self.rect)

class Bomb(pygame.sprite.Sprite):
    def __init__(self,type,pos,order=0) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.type=type
        if type=='zang':
            image=pygame.image.load(r'img\zang2.png')
            self.image=pygame.transform.scale(image,(250,250))
            self.rect=self.image.get_rect()
            self.rect.topleft=(pos[0]-self.rect.width/2,pos[1]-self.rect.height/2)
            self.hong=25
            self.count=0

    def display(self):
        scr.blit(self.image,self.rect)

class Manager(object):
    def __init__(self) -> None:
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont(['仿宋_GB2312','Times New Roman'],50,True,False)
        self.status=0
    
    def start(self):
        background=pygame.image.load(r'img\background.jpg')
        scale_background=pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
        background_rect=background.get_rect()
        background_rect.topleft=(0,0)
        title=pygame.image.load(r'img\title.png')
        scale_title=pygame.transform.scale(title,(800,200))
        title_rect=scale_title.get_rect()
        title_rect.topleft=(200,50)
        start_btn=pygame.image.load(r'img\start_btn.png')
        scale_start_btn=pygame.transform.scale(start_btn,(200,200))
        start_btn_rect=scale_start_btn.get_rect()
        start_btn_rect.topleft=(600,300)
        scale_help_btn=pygame.transform.scale(pygame.image.load(r'img\help_btn.png'),(200,200))
        help_btn_rect=scale_help_btn.get_rect()
        help_btn_rect.topleft=(600,600)

        while True:
            self.clock.tick(60)
            scr.blit(scale_background,background_rect)
            scr.blit(scale_title,title_rect)
            scr.blit(scale_start_btn,start_btn_rect)
            scr.blit(scale_help_btn,help_btn_rect)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.font.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    pos=event.pos
                    if start_btn_rect.collidepoint(pos[0],pos[1]):
                        self.status=1
                        #print(1)
                    elif help_btn_rect.collidepoint(pos[0],pos[1]):
                        self.status=2
                        #print(2)
            pygame.display.update()
            if self.status!=0:
                break

    def choose(self):
        background=pygame.image.load(r'img\background.jpg')
        scale_background=pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
        background_rect=background.get_rect()
        background_rect.topleft=(0,0)
        title=self.font.render('请选择你的英雄',True,(0,0,0))
        scale_title=pygame.transform.scale(title,(600,200))
        title_rect=scale_title.get_rect()
        title_rect.topleft=(350,30)
        zang_image=pygame.transform.scale(pygame.image.load(r'img\zang0.png'),(300,300))
        zang_rect=zang_image.get_rect()
        zang_rect.topleft=(150,300)
        name=pygame.transform.scale(self.font.render('奶志达',True,(0,0,0),(0,128,0)),(300,100))
        name_rect=name.get_rect()
        name_rect.topleft=(150,700)
        see=''
        while True:
            self.clock.tick(60)
            scr.blit(scale_background,background_rect)
            scr.blit(scale_title,title_rect)
            scr.blit(zang_image,zang_rect)
            scr.blit(name,name_rect)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.font.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    pos=event.pos
                    if name_rect.collidepoint(pos[0],pos[1]):
                        see='zang'
                        texts=['奶志达技能介绍：',
                        '初始血量：100 初始攻击：1',
                        '近战机制：对周围一圈的敌人造成击退，并吸取血量',
                        '必杀技：狂战',
                        '',
                        '',
                        '开始游戏',
                        '返回']
                    elif see=='zang':
                        if pygame.Rect(900,300+60*6,200,50).collidepoint(pos[0],pos[1]):
                            self.status=3
                        elif pygame.Rect(900,300+60*7,100,50).collidepoint(pos[0],pos[1]):
                            see=''
                                            
            if see=='zang':
                i=-1
                for text in texts:
                    search=self.font.render(text,True,(0,0,0))
                    i+=1
                    if i==6 or i==7:
                        scr.blit(search,(900,300+60*i,800,800))
                    else:
                        scr.blit(search,(500,300+60*i,800,800))

            if self.status!=1:
                break
            pygame.display.update()

    def help(self):
        background=pygame.image.load(r'img\background.jpg')
        scale_background=pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
        background_rect=background.get_rect()
        background_rect.topleft=(0,0)
        teach=pygame.transform.scale(pygame.image.load(r'img\teach.png'),(800,700))
        teach_rect=teach.get_rect()
        teach_rect.topleft=(200,30)
        back=pygame.transform.scale(pygame.image.load(r'img\back.png'),(200,200))
        back_rect=back.get_rect()
        back_rect.topleft=(900,650)
        while True:
            self.clock.tick(60)
            scr.blit(scale_background,background_rect)
            scr.blit(teach,teach_rect)
            scr.blit(back,back_rect)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.font.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    pos=event.pos
                    if back_rect.collidepoint(pos[0],pos[1]):
                        self.status=0
            pygame.display.update()
            if self.status!=2:
                break

    def over(self):
        global score
        background=pygame.image.load(r'img\background.jpg')
        scale_background=pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
        background_rect=background.get_rect()
        background_rect.topleft=(0,0)
        image=pygame.transform.scale(pygame.image.load(r'img\zang0.png'),(500,500))
        image_rect=image.get_rect()
        image_rect.topleft=(100,350)
        texts=['你挂了',
               '最终得分：'+str(score),
               '返回主界面']
        while True:
            self.clock.tick(60)
            scr.blit(scale_background,background_rect)
            scr.blit(image,image_rect)
            i=-1
            for text in texts:
                i+=1
                if i==0:
                    search=pygame.transform.scale(self.font.render(text,True,(0,0,0)),(250,250))
                    scr.blit(search,(600,60,800,800))
                elif i==1:
                    search=pygame.transform.scale(self.font.render(text,True,(0,0,0)),(600,50))
                    scr.blit(search,(700,450,800,800))
                
                elif i==2:
                    search=pygame.transform.scale(self.font.render(text,True,(0,0,0)),(250,50))
                    scr.blit(search,(800,650,800,800))
                
                else:
                    search=pygame.transform.scale(self.font.render(text,True,(0,0,0)),(250,50))
                    scr.blit(search,(500,300+60*i,800,800))

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.font.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    pos=event.pos
                    if pygame.Rect(800,650,250,50).collidepoint(pos[0],pos[1]):
                        self.status=0
            if self.status!=4:
                break
            pygame.display.update()


    def game(self):
        global score
        score=0
        background=pygame.image.load(r'img\background.jpg')
        scale_background=pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
        background_rect=background.get_rect()
        background_rect.topleft=(0,0)
        have=pygame.image.load(r'img\fight.png')
        wait=pygame.image.load(r'img\wait.png')
        scale_have=pygame.transform.scale(have,(50,50))
        scale_wait=pygame.transform.scale(wait,(50,100))
        have_rect=(SCREEN_WIDTH-180,360,50,50)
        wait_rect=(SCREEN_WIDTH-180,360,50,160)
        player1=player('zang')
        goat_group=pygame.sprite.Group()
        watermelon_group=pygame.sprite.Group()
        star_group=pygame.sprite.Group()
        global enemy_list
        enemy_list=pygame.sprite.Group()
        count=0
        while True:
            self.clock.tick(60)
            count+=1
            if count>=10000:
                count=0
            scr.blit(scale_background,background_rect)
            score_image=self.font.render(str(score),True,(0,0,0))
            score_rect=score_image.get_rect()
            score_rect.topleft=(SCREEN_WIDTH-180,600)

            scr.blit(score_image,score_rect)
            blood_image=self.font.render(str(player1.blood),True,(0,0,0))
            blood_rect=blood_image.get_rect()
            blood_rect.topleft=(SCREEN_WIDTH-250,200)

            if player1.has_crazy==True:
                scr.blit(scale_have,have_rect)
            else:
                scr.blit(scale_wait,wait_rect)

            scr.blit(blood_image,blood_rect)
            player1.display()
            player1.move()
            player1.attack()
            player1.is_shot()
            if player1.blood<=0:
                self.status=4

            if count%(200+random.randint(-5,5))==0:
                m_goat=goat()
                goat_group.add(m_goat)
                enemy_list.add(m_goat)
            for m_goat in goat_group:
                m_goat.auto_move(player1)
                m_goat.shoot(player1)
                m_goat.is_shot(player1.bullets)
                m_goat.display()
                if m_goat.live==False:
                    score+=m_goat.score
                    goat_group.remove(m_goat)
                    enemy_list.remove(m_goat)
                   
            if count%(200+random.randint(-5,5))==0:
                m_watermelon=watermelon()
                watermelon_group.add(m_watermelon)
                enemy_list.add(m_watermelon)
            for m_watermelon in watermelon_group:
                m_watermelon.auto_move(player1)
                m_watermelon.is_shot(player1.bullets)
                m_watermelon.display()
                if m_watermelon.live==False:
                    score+=m_watermelon.score
                    watermelon_group.remove(m_watermelon)
                    enemy_list.remove(m_watermelon)
                    

            if count%(400+random.randint(-10,10))==0:
                m_star=star()
                star_group.add(m_star)
                enemy_list.add(m_star)
            for m_star in star_group:
                m_star.auto_move(player1)
                m_star.shoot(player1)
                m_star.display()
                m_star.is_shot(player1.bullets)
                if m_star.live==False:
                    score+=m_star.score
                    star_group.remove(m_star)
                    enemy_list.remove(m_star)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.font.quit()
                    pygame.quit()
                    sys.exit()
            if self.status!=3:
                break
            pygame.display.update()
         
if __name__=='__main__':
    pygame.init()
    pygame.font.init()
    scr=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('FIGHT')
    icon_image=pygame.image.load(r'img\zang1.png')
    pygame.display.set_icon(icon_image)
    manager=Manager()
    while True:
        if manager.status==0:
            manager.start()
        elif manager.status==1:
            manager.choose()
        elif manager.status==2:
            manager.help()
        elif manager.status==3:
            manager.game()
        elif manager.status==4:
            manager.over()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
            pygame.display.update()
    