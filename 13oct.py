import numpy as np
import random
import copy
import matplotlib.animation as animation
import matplotlib.pyplot as plt 

fig1=plt.figure()
N=50#size of the grid
#we can make nonsquare grids if we have thath Nx is different to Ny.
Nx=N
Ny=N
steps=20
steps*=1000
f=10


grid=np.zeros((Nx,Ny)) 
fgrid=np.zeros((Nx,Ny))+f
lifegrid=np.zeros((Nx,Ny))
sgrid=np.zeros((Nx,Ny)) #signal grid
lc=[]#list with the colonies
lg=[]
ggrid=np.zeros((Nx,Ny))

class colonia:
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.pos=(x,y)
        self.life=1
        self.pvec=[]#list of the neighbours positions + it owns in the [0]
        self.vec=[]#list of values of the neighbours in a grid
    
    def obs(self):#setup of pvec->position of the neighbours
        self.pvec=[self.pos,"c","c","c","c"]        
        if self.x<Nx-1:
            self.pvec[1]=(self.x +1,self.y)#down
        if self.y<Ny-1:
            self.pvec[2]=(self.x,self.y +1)#right
        if self.x>0:
            self.pvec[3]=(self.x -1,self.y)#up
        if self.y>0:
            self.pvec[4]=(self.x,self.y -1)#left
            
    def veci(self,grid):#setup of the list vec-> vec is a list with the values of the of the positions of the list pvec in a grid
        self.vec=["c","c","c","c"]        
        for i in range(4):
            if self.pvec[i+1]!="c":
                self.vec[i]=grid[self.pvec[i+1]]
            
    def div(self,k):#find a cero in the list vec
        
        for i in range(4):
            if self.vec[i]==0:
                k.append(i+1)
        if len(k)==0:
            k.append(0)
        
        
    def eat(self):
        if fgrid[self.pos]>=1:
            fgrid[self.pos]-=1
            self.life+=1
            lifegrid[self.pos]+=1
        else:
            self.life-=1
            lifegrid[self.pos]-=1
        
    def die(self,n):
        grid[lc[n].pos]=0
        lifegrid[lc[n].pos]=0
        del lc[n]    
        
class grilla:
    def __init__(self,grid,lc,sgrid):
        self.grid=grid
        self.lc=lc
        self.sgrid=sgrid
    def updatediv(self,n):
        aux=[]#list that is going to have the index of the ceros y pvec list
        self.lc[n].obs()
        self.lc[n].veci(self.grid)
        self.lc[n].div(aux)
        aux2=random.choice(aux)#choose a random index
        c=self.lc[n].pvec[aux2]
        # c is a position in the grid with a cero, neighbour to de colony
        
        self.divforce(n,c)
        fgrid[self.lc[n].pos]-=2
            
    def divforce(self,n,c):       
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
        
        #Loop where the colony give life counters to it neighbours
        for posi in self.lc[m].pvec:
            for l in range(len(self.lc)):
                if posi == self.lc[l].pos:
                    self.lc[l].life+=1
                    lifegrid[self.lc[l].pos]+=1
                    self.lc[m].life-=1
                    lifegrid[self.lc[m].pos]-=1
        
        
        #divition loop of the sandpile
        aux3=[]
        self.lc[m].div(aux3)
        for i in aux3:
            c=self.lc[m].pvec[i]
            if c != self.lc[m].pos:
                self.divforce(m,c)
                self.lc[m].life-=1
                lifegrid[self.lc[m].pos]-=1




                

class gusano:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.pos=(x,y)
        self.pvec=[]#list of the neighbours positions + it owns in the [0]
        self.vec=[]#list of values of the neighbours in a grid
    
    def obs(self):#setup of pvec->position of the neighbours
        self.pvec=[self.pos,"c","c","c","c"]        
        if self.x<Nx-1:
            self.pvec[1]=(self.x +1,self.y)#down
        if self.y<Ny-1:
            self.pvec[2]=(self.x,self.y +1)#right
        if self.x>0:
            self.pvec[3]=(self.x -1,self.y)#up
        if self.y>0:
            self.pvec[4]=(self.x,self.y -1)#left
    
    def veci(self,grid):#setup of the list vec-> vec is a list with the values of the of the positions of the list pvec in a grid
        self.vec=["c","c","c","c"]        
        for i in range(4):
            if self.pvec[i+1]!="c":
                self.vec[i]=grid[self.pvec[i+1]]


    def ceros(self,k):#function to find ceros in the list vec
        for i in range(4):
            if self.vec[i]==0:
                k.append(i+1) 
        if len(k)==0:
            k.append(0)
 
    def move(self,aux2):
        aux1=[]#list that will have the ceros around the womr's position
        self.obs()
        self.veci(grid)              
        self.ceros(aux1)
        
        if len(aux1)!=0:
            aux2=random.choice(aux1)
            
            ggrid[self.pos]-=1
            grid[self.pos]-=6
            grid[self.pvec[aux2]]=6
            ggrid[self.pvec[aux2]]=1
            self.pos=self.pvec[aux2]
            self.x=self.pvec[aux2][0]
            self.y=self.pvec[aux2][1]

        
    def eat(self):
        self.obs()
        self.veci(grid)
        aux1=[]
        for i in range(1,5):
            if self.pvec[i] != "c":
                if grid[self.pvec[i]]!=0:
                    aux1.append(self.pvec[i])
                    
                   
        if len(aux1)!=0:
            aux2=random.choice(aux1)
            grid[aux2]=0
            lifegrid[aux2]=0
            for col in lc:
                if col.pos==aux2:
                   lc.remove(col) 
            
        
        
def compute_laplacian_x(x):
    w,h=x.shape
    Lx=np.zeros_like(x)
    for i in range(w):
        for j in range(h):
            Lx[i,j]=4*x[i,j]
            if i>0:
                Lx[i,j]-=x[i-1,j]
            else:
                Lx[i,j]-=x[-1,j]
            
            if i<w-1:
                Lx[i,j]-=x[i+1,j]
            else:
                Lx[i,j]-=x[0,j]
                
            if j>0:
                Lx[i,j]-=x[i,j-1]
            else:
                Lx[i,j]-=x[i,-1]
            
            if j<w-1:
                Lx[i,j]-=x[i,j+1]
            else:
                Lx[i,j]-=x[i,0]
    return Lx*0.25


worm=gusano(Nx//2,Ny//2)#here we setup the worm in the middle of the grid
grid[Nx//2,Ny//2]=6
ggrid[Nx//2,Ny//2]=1

for i in range(5):#loop to set the initial conditions, the if is to be sure that we are not going to have a colony over the worm
    a=random.randint(0,Nx-1)
    b=random.randint(0,Ny-1)
    if a!=Nx/2 and b!=Ny/2:
        grid[a,b]=i+1
        lifegrid[a,b]=1
        lc.append(colonia(a,b,i+1))


            
lattice=grilla(grid,lc,sgrid)
step=1
ims1=[]
p2=1#eat prob
p3=0.05#div prob
p4=1e-2#signal prob
p5=1e-3#apear new food prob
p6=5e-2#move wormprob
cont=0
while step<steps:
    if random.uniform(0,1)<=p6:
        aux2=0
        worm.move(aux2)

    worm.eat()

    if len(lc)==0:
        break
    
    if random.uniform(0,1)<=p5:
        fgrid+=1
    
    n1=random.randint(0,len(lc)-1)
    dead=0
    
    '''#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #SIGNAL CICLE:
    '''
    
    if random.uniform(0,1)<=p4:
        sgrid[lc[n1].pos]+=1
    
    sgrid=sgrid-compute_laplacian_x(sgrid)*0.1
    
    
    '''#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #EAT CICLE AND SANDPILE:
    '''
    
    if random.uniform(0,1)<=p2:
        lc[n1].eat()
        if lc[n1].life==0:
            lc[n1].die(n1)
            dead=1
            
    if len(lc)==0:
        break    
        
        
    if dead==0 and lc[n1].life>=8:
        lattice.sandpile(n1)
    
    '''#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #DIVIDE CICLE:
    '''
    if dead==0 and random.uniform(0,1)<=p3 and fgrid[lc[n1].pos]>=2 :
        lattice.updatediv(n1)


        
    
    if step//100==float(step)/100:#making the animations, the 100 is to have less "photos" of the system evolution
            im1 = plt.imshow(copy.copy(grid),animated=True,interpolation='nearest',clim=[0,6])
            ims1.append([im1])

    step+=1
    

ani1 = animation.ArtistAnimation(fig1, ims1, interval=1, blit=True,repeat_delay=0)#interval ~ time between frames
plt.show()