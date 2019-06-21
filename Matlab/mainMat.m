clc
close all
clear
pause(0.1)

%%INTEGRACIÓN----------------------
%Condiciones iniciales y parámetros
s=0.0001;
L=10000;
M=1000;
p.dx=0.5/M;
p.c=5;
x_vect=linspace(0,p.dx*M,M);
time_int=linspace(0,s*L,L);

CI=zeros(2,1,M);
% CI(1,1,10)=1;
% CI(1,1,M-10)=2;
% CI(1,1,M-15)=3;
CI(2,1,2)=10000;

%Inicio de la integración
U=zeros(2,L,M);
k=1;
U(:,k,:)=CI;
k=2;  %Iniciamos con Euler
[F]=wave1( CI,p);
U(:,k,:)=U(:,k-1,:)+s*F;

time(1,L)=0;time(2,L)=s;

for k=3:L;
    %Runge Kutta 4 hasta el final
    [K1]=wave1( U(:,k-1,:),p);
    [K2]=wave1( U(:,k-1,:)+s*0.5*K1,p);
    [K3]=wave1( U(:,k-1,:)+s*0.5*K2,p);
    [K4]=wave1( U(:,k-1,:)+s*K3,p);
    U(:,k,:)=U(:,k-1,:)+s/6*(K1+2*K2+2*K3+K4);

    time(1,k)=s*(k-1);
end

aux=zeros(L,M);
aux(:,:)=U(1,:,:);

figure(1)

for k=1:L
plot(x_vect,aux(k,:)),grid minor,axis([min(x_vect) max(x_vect) -0.5 0.5]);
pause(0.0001)
end


figure(2)

h=surf(aux);
set(h,'edgecolor','none')

max(max(aux))
