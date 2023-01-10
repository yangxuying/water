function Final = WQI(data)
[nn,mm]=size(data);
Final=ones(1,mm);
cp=[];
%level=[];
[n,m]=size(data);
  for i = 1:n
      for j = 1:m
          if j==1
              if data(i,j)>=7.5
                  I=100;
              end
              if 7<data(i,j)&&data(i,j)<7.5
                  I=90;
              end
              if 6.5<data(i,j)&&data(i,j)<=7
                  I=80;
              end
              if 6<data(i,j)&&data(i,j)<=6.5
                  I=70;
              end
              if 5<data(i,j)&&data(i,j)<=6
                  I=60;
              end
              if 4<data(i,j)&&data(i,j)<=5
                  I=50;
              end
              if 3.5<data(i,j)&&data(i,j)<=4
                  I=40;
              end
              if 3<data(i,j)&&data(i,j)<=3.5
                  I=30;
              end
              if 2<data(i,j)&&data(i,j)<=3
                  I=20;
              end
              if 1<=data(i,j)&&data(i,j)<=2
                  I=10;
              end
               if data(i,j)<1
                  I=0;
               end
               cp(1,j)=I*4;
               %cp(1,j)=I*3;
          end
          if j==2
              if data(i,j)<1
                I=100;
              end
               if 1<=data(i,j)&&data(i,j)<2
                I=90;
               end
               if 2<=data(i,j)&&data(i,j)<3
                I=80;
               end
               if 3<=data(i,j)&&data(i,j)<4
                I=70;
               end
               if 4<=data(i,j)&&data(i,j)<5
                I=60;
               end
               if 5<=data(i,j)&&data(i,j)<8
                I=50;
               end
               if 8<=data(i,j)&&data(i,j)<10
                I=40;
               end
               if 10<=data(i,j)&&data(i,j)<12
                I=30;
               end
               if 12<=data(i,j)&&data(i,j)<14
                I=20;
               end
               if 14<=data(i,j)&&data(i,j)<15
                I=10;
               end
               if data(i,j)>15
                  I=0;
               end
               cp(1,j)=I*3;
          end
          if j==3
              if data(i,j)<0.5
                I=100;
              end
              if 0.5<=data(i,j)&&data(i,j)<2
                I=90;
              end
               if 2<=data(i,j)&&data(i,j)<3
                I=80;
               end
               if 3<=data(i,j)&&data(i,j)<4
                I=70;
               end
               if 4<=data(i,j)&&data(i,j)<5
                I=60;
               end
               if 5<=data(i,j)&&data(i,j)<6
                I=50;
               end
               if 6<=data(i,j)&&data(i,j)<8
                I=40;
               end
               if 8<=data(i,j)&&data(i,j)<10
                I=30;
               end
               if 10<=data(i,j)&&data(i,j)<12
                I=20;
               end
               if 12<=data(i,j)&&data(i,j)<15
                I=10;
               end
               if data(i,j)>15
                  I=0;
               end
               cp(1,j)=I*3;
          end
          if j==4
              if data(i,j)<0.01
                I=100;
              end
               if 0.01<=data(i,j)&&data(i,j)<0.05
                I=90;
               end
               if 0.05<=data(i,j)&&data(i,j)<0.1
                I=80;
               end
               if 0.1<=data(i,j)&&data(i,j)<0.2
                I=70;
               end
               if 0.2<=data(i,j)&&data(i,j)<0.3%%%%%
                I=60;
               end
               if 0.3<=data(i,j)&&data(i,j)<0.4
                I=50;
               end
               if 0.4<=data(i,j)&&data(i,j)<0.5
                I=40;
               end
               if 0.5<=data(i,j)&&data(i,j)<0.75
                I=30;
               end
               if 0.75<=data(i,j)&&data(i,j)<1
                I=20;
               end
               if 1<=data(i,j)&&data(i,j)<1.25
                I=10;
               end
               if data(i,j)>1.25
                  I=0;
               end
               cp(1,j)=I*4;
          end
          if j==5
              if data(i,j)<0.01
                I=100;
              end
               if 0.01<=data(i,j)&&data(i,j)<0.02
                I=90;
               end
               if 0.02<=data(i,j)&&data(i,j)<0.05
                I=80;
               end
               if 0.05<=data(i,j)&&data(i,j)<0.1
                I=70;
               end
               if 0.1<=data(i,j)&&data(i,j)<0.15
                I=60;
               end
               if 0.15<=data(i,j)&&data(i,j)<0.2
                I=50;
               end
               if 0.2<=data(i,j)&&data(i,j)<0.25
                I=40;
               end
               if 0.25<=data(i,j)&&data(i,j)<0.3
                I=30;
               end
               if 0.3<=data(i,j)&&data(i,j)<0.35
                I=20;
               end
               if 0.35<=data(i,j)&&data(i,j)<=0.4
                I=10;
               end
               if data(i,j)>0.4
                  I=0;
               end
               cp(1,j)=I*4;
          end
          WQI=sum(cp)/18;
          Z{i}=WQI;
          if 85<WQI
              level=1;
          end
          if 70<WQI&&WQI<=85
              level=2;
          end
          if 50<WQI&&WQI<=70
              level=3;
          end
          if 25<=WQI&&WQI<=50
              level=4;
          end
          if WQI<25
              level=5;
          end
%           if 80<WQI
%               level='Ⅰ';
%           end
%           if 60<WQI&&WQI<=80
%               level='Ⅱ';
%           end
%           if 40<WQI&&WQI<=60
%               level='Ⅲ';
%           end
%           if 20<=WQI&&WQI<=40
%               level='Ⅳ';
%           end
%           if WQI<20
%               level='Ⅴ';
%           end
          Final(1,i)=level;
%           A=cell2mat(Final);%将元胞数组转化为矩阵
%           fprintf('%c',A);输出数组
      end
  end
