from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import animation
import imageio
import ffmpeg
   
       
class Simulation:

  def __init__(self, dt=0.0001,c=100,T=1000,Xsteps=100,Ysteps=100,
                    Xlength=0.5,Ylength=0.5,prop_eq="1D"):

    self.dt=dt
    self.Lx=Xlength
    self.Ly=Ylength
    self.Xsteps=Xsteps
    self.Ysteps=Ysteps
    self.dx=self.Lx/Xsteps
    self.dy=self.Ly/Ysteps
    self.c=c
    self.T=T
    self.CI=0
    if prop_eq=="1D":
      self.prop=self.wave1
    elif prop_eq=="2D":
      self.prop=self.wave2


  # -------- READ POSITION FROM VECTOR AND CREATE SKYDEL OBJECT -------------
  def euler(self, U):

    U=U+self.dt*self.prop(U)

    return U
    
  def RK4(self, U):

    #Runge Kutta 4 hasta el final
    K1=self.prop(U);
    K2=self.prop(U+self.dt*0.5*K1);
    K3=self.prop(U+self.dt*0.5*K2);
    K4=self.prop(U+self.dt*K3);
    
    U=U+self.dt/6*(K1+2*K2+2*K3+K4);

    return U
    
  def ABM2(self, U1, U0):

    #Predictor Adam Bashford
    Fn0=self.prop(U0);
    Fn1=self.prop(U1);
    U=U1+self.dt/2*(3*Fn1-Fn0);
    #Corrector Adam Moulton
    Fn=self.prop(U);
    U=U1+self.dt/2*(Fn+Fn1);

    return U

  def wave1(self, U):

    dU=np.zeros((2,self.Xsteps));
    dU[0,:]=U[1,:];
    
    for i in range(1,self.Xsteps-2):
      dU[1,i]=(self.c/self.dx)**2*(U[0,i+1]-2*U[0,i]+U[0,i-1])/2-10*(U[1,i]);
    
    dU[:,0]=0;
    dU[:,self.Xsteps-1]=0;

    return dU
    
  def wave2(self, U):

    dU=np.zeros((2,self.Xsteps,self.Ysteps));
    dU[0,:,:]=U[1,:,:];
    
    for j in range(1,self.Ysteps-2):
      for i in range(1,self.Xsteps-2):
        dU[1,i,j]=(self.c**2)*((U[0,i+1,j]-2*U[0,i,j]+U[0,i-1,j])/self.dx**2
        +(U[0,i,j+1]-2*U[0,i,j]+U[0,i,j-1])/self.dy**2)/2-10*(U[1,i,j]);

    return dU
    
  def init_cond(self, CI):

    self.CI=CI

    return self.CI


if __name__ == "__main__":
   

#---------------- INTEGRACIÓN ----------------------
#Condiciones iniciales y parámetros
  mode="2D"

  sim_args = {"dt" : 0.00001,
              "T" : 700,
              "prop_eq" : mode,
              "Xsteps" : 20,
              "Ysteps" : 20}
  
  p=Simulation(**sim_args);
  
  x_vect=np.linspace(0,p.dx*p.Xsteps,p.Xsteps);
  y_vect=np.linspace(0,p.dy*p.Ysteps,p.Ysteps);
  time_int=np.linspace(0,p.dt*p.T,p.T);


  
  if mode=="1D":
    CI=np.zeros((2,1,p.Xsteps))
    CI[0,0,2]=1
    CI[0,0,int(p.Xsteps/2)]=0.5
#Inicio de la integración
    U=np.zeros((2,p.T,p.Xsteps))
    p.init_cond(CI)
    U[:,0,:]=CI[:,0,:]
    U[:,1,:]=p.euler(U[:,0,:])
    U[:,2,:]=p.euler(U[:,1,:])
  elif mode=="2D":  
    CI=np.zeros((2,1,p.Xsteps,p.Ysteps))
    CI[0,0,2,0]=1
    CI[0,0,int(p.Xsteps/2),int(p.Ysteps/2)]=0.5
#Inicio de la integración
    U=np.zeros((2,p.T,p.Xsteps,p.Ysteps))
    p.init_cond(CI)
    U[:,0,:,:]=CI[:,0,:,:]
    U[:,1,:,:]=p.euler(U[:,0,:,:])
    U[:,2,:,:]=p.euler(U[:,1,:,:])
  
  print_count=0
  for k in range(3,p.T-1):

    #U[:,k,:]=p.RK4(U[:,k-1,:])
    U[:,k,:,:]=p.ABM2(U[:,k-1,:,:],U[:,k-2,:,:])
    #U[:,k,:]=p.ABM2(U[:,k-1,:],U[:,k-2,:])
    
    if print_count > int(p.T/10):
      print(int(k/p.T*100))
      print_count=0
    print_count=print_count+1
    
  if mode=="1D":
    maxlim=np.amax(U[0,10:])
    minlim=np.amin(U[0,10:])
  
    for k in range(0,p.T-1,30):
      plt.plot(x_vect, U[0,k,:], 'b-')
      plt.axis([min(x_vect), max(x_vect), minlim, maxlim])
      #plt.axis([min(x_vect), max(x_vect), -1000, 1000])
      plt.pause(0.001)
      plt.clf()
    plt.draw()
    
  elif mode=="2D":  
    maxlim=np.amax(U[0,10:,:])
    minlim=np.amin(U[0,10:,:])
    X, Y = np.meshgrid(x_vect, y_vect)
    print("Creating video")
    #plt.ion()

    #fig.show()
    aux=np.zeros((p.Xsteps,p.Ysteps))

# To save this second animation with some metadata, use the following command:
    fig2 = plt.figure()

    x = np.arange(-9, 10)
    y = np.arange(-9, 10).reshape(-1, 1)
    base = np.hypot(x, y)
    ims = []
    for add in np.arange(0,p.T-1,1):
      #ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))
      aux=U[0,add,:,:];
      ims.append((plt.pcolor(x_vect, y_vect, aux),))

    im_ani = animation.ArtistAnimation(fig2, ims, interval=1, repeat_delay=3000,
                                   blit=True)
    plt.rcParams['animation.ffmpeg_path'] = 'C:/Users/ADCP/Downloads/ffmpeg-20190704-43e0ddd-win64-static/bin/ffmpeg.exe'
    FFwriter=animation.FFMpegWriter(fps=10, extra_args=['-vcodec', 'libx264'])
    im_ani.save('./im.mp4', writer=FFwriter)
    #plt.show()




      


  
  
  
  
  
  
  
  
  
  
