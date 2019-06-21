function [ dU ] = wave1( U,p )
%wave1 Summary of this function goes here
%   Detailed explanation goes here

M=size(U,3);
dU=zeros(2,1,M);

dU(1,1,:)=U(2,1,:);


for i=2:M-1
    
    dU(2,1,i)=(p.c/p.dx)^2*(U(1,1,i+1)-2*U(1,1,i)+U(1,1,i-1))/2+100*(U(1,1,i+1)-U(1,1,i-1))/2/p.dx;
    
end
 dU(:,1,1)=0;
 dU(:,1,M)=0;
end

