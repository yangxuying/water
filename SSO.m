function Index=SSO(x,a)
[z,xd] = normalizef(x);
[n,m] = size(x);
Index=ones(1,m);
for i = 1:n
    asum = 0;
    for j = 1:m
        asum = asum + a(j)*xd(i,j);
        A{i}=asum;
    end
    z(i) = asum/sum(a);
    disp(z(i))
    zf=z(1:i-5);
end

 %判断等级
  [c,d] = size(zf);
   [a,b] = size(z);
     for i = 1:c
        for j = 1:d
          if zf(i,j)>=z(i,b-4)
              index=1;
          end
          if zf(i,j)>=z(i,b-3)&&zf(i,j)<z(i,b-4)
              index=2;
          end
          if zf(i,j)>=z(i,b-2)&&zf(i,j)<z(i,b-3)
              index=3;
          end
          if zf(i,j)>=z(i,b-1)&&zf(i,j)<z(i,b-2)
              index=4;
          end
          if zf(i,j)>=z(i,b)&&zf(i,j)<z(i,b-1)
              index=5;
          end
          Index(1,j)=index;
        end
     end

function [z,xd] = normalizef( x )
 [n,m] = size(x);
x_min = zeros(1,m);
x_max = zeros(1,m);
z = zeros(1,n);
 for j = 1:m
    x_min(j) = min(x(:,j));
    x_max(j) = max(x(:,j));
 end
for i = 1:n
    for j = 1:m
 %更改
     if j==1 %溶解氧
        xd(i,j) = (x(i,j)-0.2)/(75-0.2);
     end
     if j==2 %高锰酸盐
        xd(i,j) = (150-x(i,j))/(150-0.2);
     end
     if j==3 %五日生化需氧量
        xd(i,j) = (100-x(i,j))/(100-0.2);
     end
     if j==4 %氨氮
        xd(i,j) = (20-x(i,j))/(20-0.015);
     end
     if j==5 %总磷
        xd(i,j) = (4-x(i,j))/(4-0.002);
    end
 %
    end
end   
end
end