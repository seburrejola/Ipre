import numpy as np
import random
import copy
import matplotlib.animation as animation
import matplotlib.pyplot as plt  


def main(ims2,N,Nx,Ny,steps,frame,f,mu,ka,z,p2,p5,p6,p7,ims1,grid,fgrid,lifegrid,lc,ls,lp,densc):

    
    for i in range(colors):
        #here we setup som lists
        ls.append(np.zeros((Nx,Ny)))
        lp.append(0.2)
        densc.append([])
        
       
    
    
    class colonia:
        def __init__(self,x,y,color):
            self.x=x
            self.y=y
            self.color=color
            self.pos=(x,y)
            self.life=1
            self.pvec=[]#neighbors positions + it owns in the [0]
            self.vec=[]#value of the neighbors in a grid
        
        def obs(self):
        #setup de pvec->here we put the position of the cell neighbors bases on its position.
            self.pvec=[self.pos,"c","c","c","c"]        
            if self.x<Nx-1:
                self.pvec[1]=(self.x +1,self.y)#down in the grid
            if self.y<Ny-1:
                self.pvec[2]=(self.x,self.y +1)#right in the grid
            if self.x>0:
                self.pvec[3]=(self.x -1,self.y)#up in the grid
            if self.y>0: 
                self.pvec[4]=(self.x,self.y -1)#left in the grid
                
        def veci(self,grid):
        #setup de vec-> here we put the values of the neighbors of the cell, in a grid
            self.vec=["c","c","c","c"]        
            for i in range(4):
                if self.pvec[i+1]!="c":
                    self.vec[i]=grid[self.pvec[i+1]]
                
        def div(self,k):
        # Here we setup a list (k) with the indexes i of list "vec[i]" with a zero
        # so in k we have the indexes of the places where we have an empty space on the grid            
            for i in range(4):
                if self.vec[i]==0:
                    k.append(i+1)    
            if len(k)==0:
                k.append(0)
    
            
            
        def eat(self):
            # this functions does the eating process of the cell
            if fgrid[self.pos]>=1:
                fgrid[self.pos]-=1
                self.life+=1
                lifegrid[self.pos]+=1
                densc[self.color][len(densc[self.color])-1]+=1.0
            else:
                self.life-=1
                lifegrid[self.pos]-=1
                densc[self.color][len(densc[self.color])-1]-=1.0
                
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
                        self.lc.append(colonia(c[0],c[1],self.lc[n].color))
                        lifegrid[c]=1
                                            
                        
                        
        def sandpile(self,m):
            self.lc[m].obs()
            self.lc[m].veci(self.grid)
            
            #This loops is to give the +1life in the neighbors of the cell with a cell on it
            for posi in self.lc[m].pvec:
                for l in range(len(self.lc)):
                    if posi == self.lc[l].pos:
                        self.lc[l].life+=1
                        lifegrid[self.lc[l].pos]+=1
                        self.lc[m].life-=1
                        lifegrid[self.lc[m].pos]-=1
            
            
            # This loops puts new cells in the system, is the same +1life
            # but in the empty spaces of the neighbors of the cell
            aux3=[]
            self.lc[m].div(aux3)
            for i in aux3:
                c=self.lc[m].pvec[i]
                if c != self.lc[m].pos:
                    self.divforce(m,c)
                    self.lc[m].life-=1
                    lifegrid[self.lc[m].pos]-=1
         
    
    class gusano:
        #the first functions, obs, veci and ceros, are the same first 3 functions of the colony class
        def __init__(self,x,y):
            self.x=x
            self.y=y
            self.pos=(x,y)
            self.pvec=[]#neighbors positions + it owns in the [0]
            self.vec=[]#value of the neighbors in a grid
        
        def obs(self):
        #setup de pvec->here we put the position of the worm neighbors bases on its position.
            self.pvec=[self.pos,"c","c","c","c"]        
            if self.x<Nx-1:
                self.pvec[1]=(self.x +1,self.y)#down in the grid
            if self.y<Ny-1:
                self.pvec[2]=(self.x,self.y +1)#right in the grid
            if self.x>0:
                self.pvec[3]=(self.x -1,self.y)#up in the grid
            if self.y>0:
                self.pvec[4]=(self.x,self.y -1)#left in the grid
        
        def veci(self,grid):
        #setup de vec-> here we put the values of the neighbors of the worm, in a grid
            self.vec=["c","c","c","c"]        
            for i in range(4):
                if self.pvec[i+1]!="c":
                    self.vec[i]=grid[self.pvec[i+1]]
    
    
        def ceros(self,k):
        # Here we setup a list (k) with the indexes i of list "vec[i]" with a zero
        # so in k we have the indexes of the places where we have an empty space on the grid            
            for i in range(4):
                if self.vec[i]==0:
                    k.append(i+1) 
            if len(k)==0:
                k.append(0)
     
        def move(self):
            aux1=[]#auxiliar list to have the zeros from .ceros() function
            self.obs()
            self.veci(grid)              
            self.ceros(aux1)
            states=[]
            probs=[]
            norm=0
            for i in aux1:
                # here we setup the normalization value for the movemment of the worm
                for l in range(colors):
                    norm+=lp[l]*ls[l][self.pvec[i]]
            if norm!=0:
                #here we setup the probability for each site
                for index in aux1:
                    states.append(index)
                    aux2=0#auxiliar to save the signal of all the colors(m) in one site(index).
                    for m in range(colors):
                        aux2+=lp[m]*ls[m][self.pvec[index]]/norm
                    
                    probs.append(aux2)
                
                newpos=self.pvec[np.random.choice(states,p=probs)]
                grid[self.pos]-=8
                grid[newpos]=8
                self.pos=newpos
                self.x=newpos[0]
                self.y=newpos[1]
                
    
    
            
        def eat(self):
            #function to make the worm eat and remove a cell from the system
            self.obs()
            self.veci(grid)
            aux1=[]
            for i in range(4):
                if self.vec[i] != "c":
                    if self.vec[i]!=0 and self.vec[i]<8:
                        aux1.append(self.pvec[i+1])
    
                    
            if len(aux1)!=0:
                aux2=random.choice(aux1)
                grid[aux2]=0
                lifegrid[aux2]=0
                for col in lc:
                    if col.pos==aux2:
                        densc[col.color][len(densc[col.color])-1]-=float(col.life)                
                        lc.remove(col) 
                
            
            
    def compute_laplacian_x(x):
        w,h=x.shape
        Lx=np.zeros_like(x)
        for i in range(w):
            for j in range(h):
                Lx[i,j]=4*x[i,j]
                if i>0:
                    Lx[i,j]-=x[i-1,j]
                #else:
                 #   Lx[i,j]-=0
                
                if i<w-1:
                    Lx[i,j]-=x[i+1,j]
                #else:
                 #   Lx[i,j]-=0
                    
                if j>0:
                    Lx[i,j]-=x[i,j-1]
                #else:
                 #   Lx[i,j]-=0
                
                if j<w-1:
                    Lx[i,j]-=x[i,j+1]
                #else:
                 #   Lx[i,j]-=0
        return Lx*0.25
    
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
            ls[i]=ls[i]-compute_laplacian_x(ls[i])*ka
            
    def update_densc1():
        #here we update the lists for the density plots of the different type of cells
        for i in range(colors):
            densc[i+1].append(densc[i+1][len(densc[i+1])-1])
    
    def update_densc2():
        #here we setup the curve of all the cells
        lifecounter=0
        for i in range(len(lc)):
            lifecounter+=lc[i].life 
        densc[0].append(float(lifecounter))
         
       
         
    '''
    Initial Conditions:     
    '''  
    
    worm=gusano(Nx//2 -2,Ny//2 -2)
    grid[Nx//2 -2,Ny//2 -2]=8
    
    worm2=gusano(Nx//2 +2,Ny//2 +2)
    grid[Nx//2 +2,Ny//2 +2]=8
    
    for i in range(colors):
        #loop to put a "colors" amount of different cells
        a=random.randint(0,Nx-1)
        b=random.randint(0,Ny-1)
        if grid[a,b]==0:
            grid[a,b]=i+1
            lifegrid[a,b]=1
            lc.append(colonia(a,b,i+1))
            densc[i+1].append(1.0)
    
    densc[0].append(float(len(lc)))       
    lattice=grilla(grid,lc,ls)
    
    
    step=1
    while step<steps:
        '''
        LOOP FOR THE SIMULATION
        '''
        if random.uniform(0,1)<=p7:#gate for the eating of the worms
            worm.eat()
            worm2.eat()
        if random.uniform(0,1)<=p6:#gate for the moving of the worms
            worm2.move()
            worm.move()

        if len(lc)==0:
            break
        update_densc1()#here we update the densitiy curve of each cell type 
        
        if random.uniform(0,1)<=p5:#gate to put new food
            fgrid+=1
        
        n1=random.randint(0,len(lc)-1)#random index to pick a random cell
        dead=0
        
        if random.uniform(0,1)<=lc[n1].signalprob(ls[lc[n1].color-1]):
            #this gate is to send a new signal
            ls[lc[n1].color-1][lc[n1].pos]+=1
        
        compute_signal()#we compute the signals
    
        if random.uniform(0,1)<=p2:#gate for the eating of the cell
            lc[n1].eat()
            if lc[n1].life==0:
                lc[n1].die(n1)
                dead=1
                
        if len(lc)==0:
            break    
            
            
        if dead==0 and lc[n1].life>=8:#gate for the sandpile
            lattice.sandpile(n1)
        
        sgrid=copy.copy(sum(ls))
        if step%frame==0:#making the animations, the "frame" is to have less "photos" of the system evolution
            print(step/frame)
            plt.subplot(211)
            im1 = plt.imshow(copy.copy(grid),animated=True,interpolation='nearest',clim=[0,8])
            ims1.append([im1])
            plt.subplot(212)
            im2 = plt.imshow(copy.copy(sgrid),animated=True,interpolation='nearest',clim=[0,8])
            ims2.append([im2])
          
        update_densc2()#here we update the densitiy curve of all the cells         
        step+=1
    
    


N=50
Nx=N#grid size
Ny=N
steps=10
steps*=1000

frame=steps/100#frames for the gif of the simulation


f=10#initial foot
mu=0.5#parameter for the prob of sending a new signal
ka=0.1#laplacian coefficient 
colors=5#number of different of type of cells
z=0.01#parameter for the prob of sending a signal

p2=1#prob eat
p5=1e-3#prob aparecer comida
p6=5e-1#prob move gusano
p7=5e-1#prob eat worm
    

for i in range(1):#this for was to make more than one simulation
    ims1=[]
    ims2=[]
    grid=np.zeros((Nx,Ny)) #the grid
    fgrid=np.zeros((Nx,Ny))+f #foodgrid
    lifegrid=np.zeros((Nx,Ny)) #life grid
    lc=[]#list of cells
    ls=[]#signal list
    lp=[]#list of prob for the choice of the worm
    densc=[[]]#list with the lists of densities
    fig1=plt.figure()#figure for the animation
    main(ims2,N,Nx,Ny,steps,frame,f,mu,ka,z,p2,p5,p6,p7,ims1,grid,fgrid,lifegrid,lc,ls,lp,densc)
    ani1 = animation.ArtistAnimation(fig1, ims1, interval=50, blit=True,repeat_delay=0)#interval ~ tiempo entre frames
    ani2 = animation.ArtistAnimation(fig1, ims2, interval=50, blit=True,repeat_delay=0)#interval ~ tiempo entre frames

    plt.figure()
    plt.plot(densc[1],'b')
    plt.plot(densc[2],'c')
    plt.plot(densc[3],'m')
    plt.plot(densc[4],'g')    
    plt.plot(densc[5],'y')   
    plt.plot(densc[0],'k')    
    plt.show()
       
    print("-------------------")
    print("simulation number:",i+1)
    print("-------------------")
    