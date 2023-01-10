function index = FCE(data)
y=[];
a=[];w=[];
[n,m] = size(data);
  for i = 1:n
%第一个指标
    for j = 1:m
          b=5/data(i,1)+data(i,2)/6+data(i,3)/4+data(i,4)/1+data(i,5)/0.2;

       if j==1%%%%%溶解氧从一级到五级的隶属度：
               if data(i,j)>=7.5  %一级水隶属度
                y(1,1) = 1;
               end
                if 6<data(i,j)&&data(i,j)<7.5
                y(1,1) = (6-data(i,j))/(6-7.5);
                end
                if data(i,j)<=6
                y(1,1) = 0;
                end
               if 6<data(i,j)&&data(i,j)<7.5 %二级水隶属度
                y(1,2) = (data(i,j)-7.5)/(6-7.5);
                end
               if data(i,j)<=6 && data(i,j)>5
                y(1,2) = (5-data(i,j))/(5-6);
               end
                if data(i,j)<=5 || data(i,j)>=7.5
                y(1,2) = 0;
                end
               if data(i,j)>5 && data(i,j)<6 %三级水隶属度
                y(1,3) = (data(i,j)-6)/(5-6);
                end
                if data(i,j)>3 && data(i,j)<=5
                y(1,3) = (3-data(i,j))/(3-5);
                end
                if data(i,j)<=3 || data(i,j)>=6
                y(1,3) = 0;
                end
               if data(i,j)>3 && data(i,j)<5 %四级水隶属度
                y(1,4) = (data(i,j)-5)/(3-5);
               end
                if data(i,j)>2 && data(i,j)<=3
                y(1,4) = (2-data(i,j))/(2-3);
                end
                if data(i,j)<=2 || data(i,j)>=5
                y(1,4) = 0;
                end
               if data(i,j)<=2 %五级水隶属度
                y(1,5) = 1;
               end
                if data(i,j)>2 && data(i,j)<3
                y(1,5) = (data(i,j)-3)/(2-3);
                end
                if data(i,j)>=3
                y(1,5) = 0;
                end
                %a(1,j)=(5/data(i,j))/b;
                w(1,j)=5/data(i,j);
                a(1,j)=w(1,j)/b;
                %(data(i,j)-av1).^2)

       end%%%%%
%第二个指标
       if j==2 %%%%%高猛酸盐从一级到五级的隶属度：
               if data(i,j)<=2 %一级水隶属度
                y(2,1) = 1;
               end
                if 2<data(i,j)&&data(i,j)<4
                y(2,1) = (4-data(i,j))/(4-2);
                end
                if data(i,j)>=4
                y(2,1) = 0;
                end
                if 2<data(i,j)&&data(i,j)<=4 %二级水隶属度
                y(2,2) = (data(i,j)-2)/(4-2);
               end
                if 4<data(i,j)&&data(i,j)<6
                y(2,2) = (6-data(i,j))/(6-4);
                end
                if data(i,j)>=6 || data(i,j)<=2
                y(2,2) = 0;
                end
                if 4<data(i,j)&&data(i,j)<=6 %三级水隶属度
                y(2,3) = (data(i,j)-4)/(6-4);
                end
                if 6<data(i,j)&&data(i,j)<10
                y(2,3) = (10-data(i,j))/(10-6);
                end
                if data(i,j)>=10 || data(i,j)<=4
                y(2,3) = 0;
                end
                if 6<data(i,j)&&data(i,j)<=10 %四级水隶属度
                y(2,4) = (data(i,j)-6)/(10-6);
                end
                if 10<data(i,j)&&data(i,j)<15
                y(2,4) = (15-data(i,j))/(15-10);
                end
                if data(i,j)>=15 || data(i,j)<=6
                y(2,4) = 0;
                end
                if data(i,j)>=15 %五级水隶属度
                y(2,5) = 1;
                end
                if 10<data(i,j)&&data(i,j)<15
                y(2,5) = (data(i,j)-10)/(15-10);
                end
                if data(i,j)<=10
                y(2,5) = 0;
                end
                %a(1,j)=(data(i,j)/6)/b;
                w(1,j)=data(i,j)/6;
                a(1,j)=w(1,j)/b;
%                 w(1,j)=sqrt(byweight2*a(1,j));
       end%%%%%
%第三个指标
       if j==3 %%%%%五日化需氧量从一级到五级的隶属度：
                if data(i,j)<=3 %一、二级水隶属度
                y(3,1) = 1;
                y(3,2) = 1;
                end
                if data(i,j)>3
                y(3,1) = 0;
                y(3,2) = 0;
                end
                if 3<data(i,j)&&data(i,j)<=4 %三级水隶属度
                y(3,3) = (data(i,j)-3)/(4-3);
                end
                if 4<data(i,j)&&data(i,j)<6
                y(3,3) = (6-data(i,j))/(6-4);
                end
                if data(i,j)>=6 || data(i,j)<=3
                y(3,3) = 0;
                end
                if 4<data(i,j)&&data(i,j)<=6 %四级水隶属度
                y(3,4) = (data(i,j)-4)/(6-4);
                end
                if 6<data(i,j)&&data(i,j)<10
                y(3,4) = (10-data(i,j))/(10-6);
                end
                if data(i,j)>=10 || data(i,j)<=4
                y(3,4) = 0;
                end
                if data(i,j)>=10 %五级水隶属度
                y(3,5) = 1;
                end
                if 6<data(i,j)&&data(i,j)<10
                y(3,5) = (data(i,j)-6)/(10-6);
                end
                if data(i,j)<=6
                y(3,5) = 0;
                end
                w(1,j)=data(i,j)/4;
                a(1,j)=w(1,j)/b;
%                 w(1,j)=sqrt(byweight3*a(1,j));
       end%%%%%
%第四个指标
        if j==4 %%%%%氨氮从一级到五级的隶属度：
               if data(i,j)<=0.15 %一级水隶属度
                y(4,1) = 1;
               end
                if 0.15<data(i,j)&&data(i,j)<0.5
                y(4,1) = (0.5-data(i,j))/(0.5-0.15);
                end
                if data(i,j)>=0.5
                y(4,1) = 0;
                end
                if 0.15<data(i,j)&&data(i,j)<=0.5 %二级水隶属度
                y(4,2) = (data(i,j)-0.15)/(0.5-0.15);
                end
                if 0.5<data(i,j)&&data(i,j)<1
                y(4,2) = (1-data(i,j))/(1-0.5);
                end
                if data(i,j)>=1 || data(i,j)<=0.15
                y(4,2) = 0;
                end
                if 0.5<data(i,j)&&data(i,j)<=1 %三级水隶属度
                y(4,3) = (data(i,j)-0.5)/(1-0.5);
                end
                if 1<data(i,j)&&data(i,j)<1.5
                y(4,3) = (1.5-data(i,j))/(1.5-1);
                end
                if data(i,j)>=1.5 || data(i,j)<=0.5
                y(4,3) = 0;
                end
                if 1<data(i,j)&&data(i,j)<=1.5 %四级水隶属度
                y(4,4) = (data(i,j)-1)/(1.5-1);
                end
                if 1.5<data(i,j)&&data(i,j)<2
                y(4,4) = (2-data(i,j))/(2-1.5);
                end
                if data(i,j)>=2 || data(i,j)<=1
                y(4,4) = 0;
                end
                if data(i,j)>=2 %五级水隶属度
                y(4,5) = 1;
                end
                if 1.5<data(i,j)&&data(i,j)<2
                y(4,5) = (data(i,j)-1.5)/(2-1.5);
                end
                if data(i,j)<=1.5
                y(4,5) = 0;
                end
               %  a(1,j)=(data(i,j)/1)/b;
               w(1,j)=data(i,j)/1;
               a(1,j)=w(1,j)/b;
%                 w(1,j)=sqrt(byweight4*a(1,j));
        end%%%%%
%第五个指标
        if j==5 %%%%%总磷从一级到五级的隶属度：
              if data(i,j)<=0.02 %一级水隶属度
                y(5,1) = 1;
               end
                if 0.02<data(i,j)&&data(i,j)<0.1
                y(5,1) = (0.1-data(i,j))/(0.1-0.02);
                end
                if data(i,j)>=0.1
                y(5,1) = 0;
                end
                if 0.02<data(i,j)&&data(i,j)<=0.1 %二级水隶属度
                y(5,2) = (data(i,j)-0.02)/(0.1-0.02);
                end
                if 0.1<data(i,j)&&data(i,j)<0.2
                y(5,2) = (0.2-data(i,j))/(0.2-0.1);
                end
                if data(i,j)>=0.2 || data(i,j)<=0.02
                y(5,2) = 0;
                end
                if 0.1<data(i,j)&&data(i,j)<=0.2 %三级水隶属度
                y(5,3) = (data(i,j)-0.1)/(0.2-0.1);
                end
                if 0.2<data(i,j)&&data(i,j)<0.3
                y(5,3) = (0.3-data(i,j))/(0.3-0.2);
                end
                if data(i,j)>=0.3 || data(i,j)<=0.1
                y(5,3) = 0;
                end
                if 0.2<data(i,j)&&data(i,j)<=0.3 %四级水隶属度
                y(5,4) = (data(i,j)-0.2)/(0.3-0.2);
                end
                if 0.3<data(i,j)&&data(i,j)<0.4
                y(5,4) = (0.4-data(i,j))/(0.4-0.3);
                end
                if data(i,j)>=0.4 || data(i,j)<=0.2
                y(5,4) = 0;
                end
                if data(i,j)>=0.4 %五级水隶属度
                y(5,5) = 1;
                end
                if 0.3<data(i,j)&&data(i,j)<0.4
                y(5,5) = (data(i,j)-0.3)/(0.4-0.3);
                end
                if data(i,j)<=0.3
                y(5,5) = 0;
                end
               % a(1,j)=(data(i,j)/0.2)/b;
               w(1,j)=data(i,j)/0.2;
               a(1,j)=w(1,j)/b;
%               w(1,j)=sqrt(byweight5*a(1,j));
        end%%%%%
%         t=sum(w,2);
%         T{i}=t;
%         TT=cell2mat(T);
%         A1c = TT';
    end

     W{i}=w.';
     WW=cell2mat(W);
     A{i}=a;%超标倍数权重
     Y{i}=y;
     D=a*y;
     Z{i}=D.';%模糊综合评价结果
     %Data{i}=D.';
     U=cell2mat(Z);
     [max_U,index]=max(U,[],1);
  end
end







  
        
        


