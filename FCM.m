function Index=FCMCluster(data,n,options)
%输入
% data    n*m矩阵，n个样本数，每个样本的维度为m
% n       标量,表示聚合中心数目，即类别数5
% options 4*1 矩阵
%   options(1):隶属度矩阵U的加权指数，>1 (缺省值: 2.0)
%   options(2):最大迭代次数
%   options(3):隶属度最小变化量，迭代终止条件
%   options(4):每次迭代是否输出信息标志

%输出
% center    聚类中心
% U         隶属度矩阵
% obj_fun   目标函数值

if nargin~=2 && nargin~=3 %nargin输入变量个数，~=不等于,判断输入参数个数只能是2个或3个
    error('Too many or too few input arguments');
end

data_n=size(data,1); %设矩阵data的维度为（x*y*z），num=x;求出data的第一维(rows)数,即样本个数233
in_n=size(data,2);%求出data的第二维(columns)数，即特征值长度


%默认参数
default_options=[2;100;1e-5;1];

%参数配置
  %如果只输入前两个参数，选用默认的参数;如果参数个数小于4，其他选用默认参数
    if nargin==2
      options=default_options;
    else
       if length(options)<4
           tmp=default_options;
           tmp(1:length(options))=options;
           options=tmp;
       end
       nan_index=find(isnan(options)==1);%返回options中是数的值为0,不是数时为1
       options(nan_index)=default_options(nan_index);%将denfault_options中对应位置的参数赋值给options中不是数的位置
       if options(1)<=1 %如果模糊矩阵的指数小于等于1
           error('The exponent should be greater than 1!');
       end
    end

%将options 中的分量分别赋值给四个变量
  expo=options(1);
  max_iter=options(2);
  min_impro=options(3);
  display=options(4);

 obj_fun=zeros(max_iter,1);% 目标函数obj_fcn的建立

%初始化模糊分配矩阵,使U满足列上相加为1
      %U=initfcm(n,data_n);
      %原始
      U=func_u(data);

      [maxdata,~]=max(data);
for j=1:n
    data(:,j)=data(:,j)/maxdata(j);
end

%     U=load('sample');
%     U=U.U;
%主程序
   for i=1:max_iter
       [U,center,obj_fun(i)]=stepfcm(data,U,n,expo);%在第k步循环中改变聚类中心ceneter,和分配函数U的隶属度值;
       if display    %如果display为真，就执行
           fprintf('FCM:Iteration count=%d,obj_fun=%f\n',i,obj_fun(i));%Iteration count迭代次数；obj_fun迭代函数，当误差小时迭代结束
       end
       %终止条件判别
       if i>1
           if abs(obj_fun(i)-obj_fun(i-1))<min_impro %如果目标函数值obj_fun<隶属度最小变化量
               break;
           end
       end
   end
   iter_n=i;%实际迭代次数
   obj_fun(iter_n+1:max_iter)=[];
   Index=ajaljsdl(U);

end
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%子函数 模糊矩阵(fcm的隶属度函数矩阵)初始化
%    %n聚类中心个数，data_n样本点数
%        function U = initfcm(n, data_n)%样本数目是n*data_n
%         U=rand(n,data_n);
%         col_sum=sum(U);
%         U=U./col_sum(ones(n,1),:);
%       end
%       function U= initfcm()
%             U=load('sample');
%             U=U.U;
%       end
%%子函数 逐步聚类(模糊C均值聚类时迭代的一步)
        function [U_new,center,obj_fun]=stepfcm(data,U,n,expo)
        %expo：隶属度矩阵U的指数
        %U_new：迭代计算出的新的隶属度矩阵，center：新的聚类中心，obj_fcn：目标函数值
            mf=U.^expo; % 隶属度矩阵进行指数运算结果
            center=mf*data./((ones(size(data,2),1)*sum(mf'))');% 新聚类中心(5.4)式
            dist=distfcm(center,data);% 计算距离矩阵
            obj_fun=sum(sum((dist.^2).*mf));% 计算目标函数值(5.1)式
            tmp=dist.^(-2/(expo-1));
            U_new=tmp./(ones(n,1)*sum(tmp));% 计算新的隶属度矩阵(5.3)式
        end
%%子函数 计算样本点距离聚类中心的距离
            function out=distfcm(center,data) % out：距离
                out=zeros(size(center,1),size(data,1));
                for k=1:size(center,1) % 对每一个聚类中心
                    % 每一次循环求得所有样本点到一个聚类中心的距离
                    out(k,:)=sqrt(sum(((data-ones(size(data,1),1)*center(k,:)).^2)',1));
                end
            end
        function Index=ajaljsdl(U)
            [nn,mm]=size(U);
            Index=ones(1,mm);
            maxU = max(U);%后加
index1=find(U(1,:)==max(U));%找出属于第一类的点
index2=find(U(2,:)==max(U));%找出划分为第二类的数据索引
index3=find(U(3,:)==max(U));%找出划分为第三类的数据索引
index4=find(U(4,:)==max(U));%找出划分为第四类的数据索引
index5=find(U(5,:)==max(U));%找出划分为第五类的数据索引


[a,b] = size(index1);
  for i = 1:a
      for j = 1:b
        Index(1,index1(i,j))=2;
      end
  end
  [c,d] = size(index2);
  for i = 1:c
      for j = 1:d
        Index(1,index2(i,j))=1;
      end
  end
  [e,f] = size(index3);
  for i = 1:e
      for j = 1:f
        Index(1,index3(i,j))=3;
      end
  end
  [g,h] = size(index4);
  for i = 1:g
      for j = 1:h
        Index(1,index4(i,j))=4;
      end
  end
    [k,l] = size(index5);
  for i = 1:k
      for j = 1:l
        Index(1,index5(i,j))=5;
      end
  end
  disp(Index);
        end
        function U = func_u(data)
y=[];
w=[];
[n,m]=size(data);
  for i = 1:n
%第一个指标
    for j = 1:m
%         b1=data(i,j)/7.5+data(i,j)/2+data(i,j)/3+data(i,j)/0.15+data(i,j)/0.02;
%         b2=data(i,j)/6+data(i,j)/4+data(i,j)/3+data(i,j)/0.5+data(i,j)/0.1;
%         b3=data(i,j)/5+data(i,j)/6+data(i,j)/4+data(i,j)/1+data(i,j)/0.2;
%         b4=data(i,j)/3+data(i,j)/10+data(i,j)/6+data(i,j)/1.5+data(i,j)/0.3;
%         b5=data(i,j)/2+data(i,j)/15+data(i,j)/10+data(i,j)/2+data(i,j)/0.4;
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
%                 w(j,1)=(data(i,j)/7.5)/b1;
%                 w(j,2)=(data(i,j)/6)/b2;
%                 w(j,3)=(data(i,j)/5)/b3;
%                 w(j,4)=(data(i,j)/3)/b4;
%                 w(j,5)=(data(i,j)/2)/b5;
                  w(j,1)=(5/data(i,j))/b;
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
%                 w(j,1)=(data(i,j)/2)/b1;
%                 w(j,2)=(data(i,j)/4)/b2;
%                 w(j,3)=(data(i,j)/6)/b3;
%                 w(j,4)=(data(i,j)/10)/b4;
%                 w(j,5)=(data(i,j)/15)/b5;
                  w(j,1)=(data(i,j)/6)/b;
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
%                 w(j,1)=(data(i,j)/3)/b1;
%                 w(j,2)=(data(i,j)/3)/b2;
%                 w(j,3)=(data(i,j)/4)/b3;
%                 w(j,4)=(data(i,j)/6)/b4;
%                 w(j,5)=(data(i,j)/10)/b5;
                w(j,1)=(data(i,j)/4)/b;
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
%                 w(j,1)=(data(i,j)/0.15)/b1;
%                 w(j,2)=(data(i,j)/0.5)/b2;
%                 w(j,3)=(data(i,j)/1)/b3;
%                 w(j,4)=(data(i,j)/1.5)/b4;
%                 w(j,5)=(data(i,j)/2)/b5;
                w(j,1)=(data(i,j)/1)/b;
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
%                 w(j,1)=(data(i,j)/0.02)/b1;
%                 w(j,2)=(data(i,j)/0.1)/b2;
%                 w(j,3)=(data(i,j)/0.2)/b3;
%                 w(j,4)=(data(i,j)/0.3)/b4;
%                 w(j,5)=(data(i,j)/0.4)/b5;
                w(j,1)=(data(i,j)/0.2)/b;
        end%%%%%
    end
     Y{i}=y;
     D=w.*y;
     A=sum(D);
     Data{i}=A.';%模糊综合评价结果
     U=cell2mat(Data);
     %save sample U
  end

end