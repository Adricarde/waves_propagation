import numpy as np
import matplotlib.pyplot as plt


class Simulation:

  def __init__(self, dt=0.0001,c=5,T=10000,Xsteps=1000):

    self.dt=dt
    self.dx=0.5/Xsteps
    self.c=c
    self.T=T
    self.Xsteps=Xsteps

  # -------- READ POSITION FROM VECTOR AND CREATE SKYDEL OBJECT -------------
  def _readRow(self, row):

    time = float(row[0]) * 1000

    yield time

  def wave1(self, row):

    time = float(row[0]) * 1000

    yield time



if __name__ == "__main__":
   
  print("Hello World!")

#---------------- INTEGRACIÓN ----------------------
#Condiciones iniciales y parámetros

  p=Simulation();
  
  x_vect=np.linspace(0,p.dx*p.Xsteps,p.Xsteps);
  time_int=np.linspace(0,p.dt*p.T,p.T);

  CI=np.zeros((2,1,p.Xsteps));

  CI[0,0,2]=1;

#Inicio de la integración
  U=np.zeros((2,p.T,p.Xsteps));
  k=1;
  print(CI.shape)
  print(U.shape)
  #U[:,k,:]=np.reshape(CI,(2,p.T));
  U[1,k,:]=CI[0,0,:]
  k=2;  #Iniciamos con Euler
  #[F]=wave1( CI,p);
  #U(:,k,:)=U(:,k-1,:)+s*F;

#time(1,L)=0;time(2,L)=s;





# evenly sampled time at 200ms intervals
  t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
  plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
  plt.show()
