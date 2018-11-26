import numpy as np
import random
import copy
import matplotlib.animation as animation
import matplotlib.pyplot as plt  
import scipy.ndimage


class colony:
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.pos=(x,y)
        self.life=1
        self.posneigh=[]#neighbors positions + it owns in the [0]
        self.neigh=[]#value of the neighbors in a grid
    
    def obs(self):
    #setup de pvec->here we put the position of the cell neighbors bases on its position.
        self.posneigh=[self.pos,"c","c","c","c"]        
        if self.x<Nx-1:
            self.posneigh[1]=(self.x +1,self.y)#down in the grid
        if self.y<Ny-1:
            self.posneigh[2]=(self.x,self.y +1)#right in the grid
        if self.x>0:
            self.posneigh[3]=(self.x -1,self.y)#up in the grid
        if self.y>0: 
            self.posneigh[4]=(self.x,self.y -1)#left in the grid
            
    def neighbors(self,grid):
    #setup de vec-> here we put the values of the neighbors of the cell, in a grid
        self.neigh=["c","c","c","c"]        
        for i in range(4):
            if self.posneigh[i+1]!="c":
                self.neigh[i]=grid[self.posneigh[i+1]]
            
    def ceros(self,k):
    # Here we setup a list (k) with the indexes i of list "vec[i]" with a zero
    # so in k we have the indexes of the places where we have an empty space on the grid            
        for i in range(4):
            if self.neigh[i]==0:
                k.append(i+1)    
        if len(k)==0:
            k.append(0)

        
        
    def eat(self):
        # this functions does the eating process of the cell
        if fgrid[self.pos]>=1:
            fgrid[self.pos]-=1
            self.life+=1
            lifegrid[self.pos]+=1
            denscolors[self.color][len(denscolors[self.color])-1]+=1.0
        else:
            self.life-=1
            lifegrid[self.pos]-=1
            denscolors[self.color][len(denscolors[self.color])-1]-=1.0
            
    def die(self,n):
        # with this function we remove the cell from the system
        grid[lc[n].pos]=0
        lifegrid[lc[n].pos]=0
        del lc[n]    
        
    def signalprob(self,sgrid):
        # this functions setups the probability of sending a signal 
        # based on the signal intensity in the position of the cell.
        prob=float(z+sgrid[self.pos]/mu)/(1 + sgrid[self.pos]/mu)
        return prob        




class grilla:
    def __init__(self,grid,lc,ls):
        self.grid=grid
        self.lc=lc
        self.ls=ls

    def divforce(self,n,c):   
        #this function puts new cells in the system
        #the new cell will have the color of lc[n] and  position c
        s=0
        if self.lc[n].life>=4:
            for i in range(len(lc)):
                if c!=self.lc[i].pos:
                    s+=1
                if s==len(lc):
                    self.grid[c]=self.lc[n].color
                    self.lc.append(colony(c[0],c[1],self.lc[n].color))
                    lifegrid[c]=1
                                        
                    
                    
    def sandpile(self,m):
        self.lc[m].obs()
        self.lc[m].neighbors(self.grid)
        
        #This loops is to give the +1life in the neighbors of the cell with a cell on it
        for posi in self.lc[m].posneigh:
            for l in range(len(self.lc)):
                if posi == self.lc[l].pos:
                    self.lc[l].life+=1
                    lifegrid[self.lc[l].pos]+=1
                    self.lc[m].life-=1
                    lifegrid[self.lc[m].pos]-=1
        
        
        # This loops puts new cells in the system, is the same +1life
        # but in the empty spaces of the neighbors of the cell
        aux3=[]
        self.lc[m].ceros(aux3)
        for i in aux3:
            c=self.lc[m].posneigh[i]
            if c != self.lc[m].pos:
                self.divforce(m,c)
                self.lc[m].life-=1
                lifegrid[self.lc[m].pos]-=1
     

class worm:
    #the first functions, obs, veci and ceros, are the same first 3 functions of the colony class
    def __init__(self,x,y,gridindex):
        self.gridindex=gridindex
        self.x=x
        self.y=y
        self.pos=(x,y)
        self.posneigh=[]#neighbors positions + it owns in the [0]
        self.neigh=[]#value of the neighbors in a grid
    
    def obs(self):
    #setup de pvec->here we put the position of the worm neighbors bases on its position.
        self.posneigh=[self.pos,"c","c","c","c"]        
        if self.x<Nx-1:
            self.posneigh[1]=(self.x +1,self.y)#down in the grid
        if self.y<Ny-1:
            self.posneigh[2]=(self.x,self.y +1)#right in the grid
        if self.x>0:
            self.posneigh[3]=(self.x -1,self.y)#up in the grid
        if self.y>0:
            self.posneigh[4]=(self.x,self.y -1)#left in the grid
    
    def neighbors(self,grid):
    #setup de vec-> here we put the values of the neighbors of the worm, in a grid
        self.neigh=["c","c","c","c"]        
        for i in range(4):
            if self.posneigh[i+1]!="c":
                self.neigh[i]=grid[self.posneigh[i+1]]


    def ceros(self,k):
    # Here we setup a list (k) with the indexes i of list "vec[i]" with a zero
    # so in k we have the indexes of the places where we have an empty space on the grid            
        for i in range(4):
            if self.neigh[i]==0:
                k.append(i+1) 
        if len(k)==0:
            k.append(0)
 
    def move(self):
        aux1=[]#auxiliar list to have the zeros from .ceros() function
        self.obs()
        self.neighbors(grid)              
        self.ceros(aux1)
        states=[]
        probs=[]
        norm=0
        for i in aux1:
            # here we setup the normalization value for the movemment of the worm
            for l in range(colors):
                norm+=lp[l]*ls[l][self.posneigh[i]]
        if norm!=0:
            #here we setup the probability for each site
            for index in aux1:
                states.append(index)
                aux2=0#auxiliar to save the signal of all the colors(m) in one site(index).
                for m in range(colors):
                    aux2+=lp[m]*ls[m][self.posneigh[index]]/norm
                
                probs.append(aux2)
            
            newpos=self.posneigh[np.random.choice(states,p=probs)]
            grid[self.pos]-=8
            grid[newpos]=8
            self.pos=newpos
            self.x=newpos[0]
            self.y=newpos[1]
            


        
    def eat(self):
        #function to make the worm eat and remove a cell from the system
        self.obs()
        self.neighbors(grid)
        aux1=[]
        for i in range(4):
            if self.neigh[i] != "c":
                if self.neigh[i]!=0 and self.neigh[i]<self.gridindex:
                    aux1.append(self.posneigh[i+1])

                
        if len(aux1)!=0:
            aux2=random.choice(aux1)
            grid[aux2]=0
            lifegrid[aux2]=0
            for col in lc:
                if col.pos==aux2:
                    denscolors[col.color][len(denscolors[col.color])-1]-=float(col.life)                
                    lc.remove(col) 
            
        



def main(ims2,N,Nx,Ny,steps,frame,f,mu,ka,z,prob_cell_eat,prob_appear_food,prob_worm_move,prob_worm_eat,ims1,grid,fgrid,lifegrid,lc,ls,lp,densc):

    
    for i in range(colors):
        #here we setup som lists
        ls.append(np.zeros((Nx,Ny)))
        lp.append(0.2)
        denscolors.append([])
        

    '''
    Here we have some functions to make the code work outside the classes
    gridmax() and gridmin() are just for testing.
    '''
    def gridmax(sgrid):
        listamax1=[]
        for i in range(len(sgrid[0])):
            listamax1.append(max(sgrid[i,:]))
        return max(listamax1)
        
    def gridmin(sgrid):
        listamax1=[]
        for i in range(len(sgrid[0])):
            listamax1.append(min(sgrid[i,:]))
        return min(listamax1)
         
    def compute_signal():
        #here we compute the signal in all the signal grids
        for i in range(len(ls)):
            ls[i]=ls[i]+scipy.ndimage.filters.laplace(ls[i],mode='constant')*0.025
            
    def update_denscolors1():
        #here we update the lists for the density plots of the different type of cells
        for i in range(colors):
            denscolors[i+1].append(denscolors[i+1][len(denscolors[i+1])-1])
    
    def update_denscolors2():
        #here we setup the curve of all the cells
        lifecounter=0
        for i in range(len(lc)):
            lifecounter+=lc[i].life 
        denscolors[0].append(float(lifecounter))
         
       
         
    '''
    Initial Conditions:     
    '''  
    
    worm1=worm(Nx//2 -2,Ny//2 -2,colors+2)
    grid[Nx//2 -2,Ny//2 -2]=colors+2
    
    worm2=worm(Nx//2 +2,Ny//2 +2,colors+2)
    grid[Nx//2 +2,Ny//2 +2]=colors+2
    
    for i in range(colors):
        #loop to put a "colors" amount of different cells
        a=random.randint(0,Nx-1)
        b=random.randint(0,Ny-1)
        if grid[a,b]==0:
            grid[a,b]=i+1
            lifegrid[a,b]=1
            lc.append(colony(a,b,i+1))
            denscolors[i+1].append(1.0)
    
    denscolors[0].append(float(len(lc)))       
    lattice=grilla(grid,lc,ls)
    
    
    
    def step(step,fgrid):
        '''
        LOOP FOR THE SIMULATION
        '''
        if random.uniform(0,1)<=prob_worm_eat:#gate for the eating of the worms
            worm1.eat()
            worm2.eat()
        if random.uniform(0,1)<=prob_worm_move:#gate for the moving of the worms
            worm1.move()
            worm2.move()

        update_denscolors1()#here we update the densitiy curve of each cell type 
        
        if random.uniform(0,1)<=prob_appear_food:#gate to put new food
            fgrid+=1
        
        n1=random.randint(0,len(lc)-1)#random index to pick a random cell
        dead=0
        
        if random.uniform(0,1)<=lc[n1].signalprob(ls[lc[n1].color-1]):
            #this gate is to send a new signal
            ls[lc[n1].color-1][lc[n1].pos]+=1
        
        compute_signal()#we compute the signals
    
        if random.uniform(0,1)<=prob_cell_eat:#gate for the eating of the cell
            lc[n1].eat()
            if lc[n1].life==0:
                lc[n1].die(n1)
                dead=1

            
            
        if dead==0 and lc[n1].life>=8:#gate for the sandpile
            lattice.sandpile(n1)
        
        sgrid=copy.copy(sum(ls))
        if step%frame==0:#making the animations, the "frame" is to have less "photos" of the system evolution
            #print(step/frame)
            plt.subplot(211)
            im1 = plt.imshow(copy.copy(grid),animated=True,interpolation='nearest',clim=[0,8])
            ims1.append([im1])
            plt.subplot(212)
            im2 = plt.imshow(copy.copy(sgrid),animated=True,interpolation='nearest',clim=[0,4])
            ims2.append([im2])
          
        update_denscolors2()#here we update the densitiy curve of all the cells         
        
        
    for i in range(steps):
        step(i,fgrid)
        if len(lc)==0:
            break
    
    


N=100
Nx=N#grid size
Ny=N
steps=1
steps*=1000
frame=steps/500#frames for the gif of the simulation

f=10#initial foot
mu=0.5#parameter for the prob of sending a new signal
ka=0.1#laplacian coefficient 
colors=5#number of different of type of cells
z=0.01#parameter for the prob of sending a signal

prob_cell_eat=1#prob eat
prob_appear_food=1e-3#prob aparecer comida
prob_worm_move=5e-1#prob move gusano
prob_worm_eat=5e-1#prob eat worm

densplots=[]
   
def ploting(densc):
    plt.figure()
    plt.plot(denscolors[1],'b')
    plt.plot(denscolors[2],'c')
    plt.plot(denscolors[3],'m')
    plt.plot(denscolors[4],'g')    
    plt.plot(denscolors[5],'y')
    plt.plot(denscolors[0],'k')    
    plt.show
       
for i in range(1):#this for was to make more than one simulation
    print("-------------------")
    print("simulation number:",i+1)
    print("-------------------")
    ims1=[]
    ims2=[]
    grid=np.zeros((Nx,Ny)) #the grid
    fgrid=np.zeros((Nx,Ny))+f #foodgrid
    lifegrid=np.zeros((Nx,Ny)) #life grid
    lc=[]#cells list
    ls=[]#signal list
    lp=[]#list of prob for the choice of the worm
    denscolors=[[]]#list with the lists of densities
    fig1=plt.figure()#figure for the animation
    main(ims2,N,Nx,Ny,steps,frame,f,mu,ka,z,prob_cell_eat,prob_appear_food,prob_worm_move,prob_worm_eat,ims1,grid,fgrid,lifegrid,lc,ls,lp,denscolors)
    ani1 = animation.ArtistAnimation(fig1, ims1, interval=50, blit=True,repeat_delay=0)#interval ~ tiempo entre frames
    ani2 = animation.ArtistAnimation(fig1, ims2, interval=50, blit=True,repeat_delay=0)#interval ~ tiempo entre frames
    densplots.append(denscolors)
    ploting(densplots[i])
    