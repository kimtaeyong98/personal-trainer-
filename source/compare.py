import pandas as pd
import math
import numpy as np

#포인트 이동 중 (0,0)으로 튄 포인트 찾아서 보정 후 다시 저장, 필요없는 문자제거
def check(path):
    data = pd.read_csv(path)
    row,column =data.shape
    row=int(row)
    column=int(column)

    for i in range(column):
        for j in range(row):
            data[str(i)][j]=data[str(i)][j].replace("(","")#(제거
            data[str(i)][j]=data[str(i)][j].replace(")","")#)제거
            
            if data[str(i)][j] =='0, 0':#0,0이 있으면 이전 값 저장
                try:#1프레임 좌표가 0,0 일 경우 에러, 일단 넘김
                    data[str(i)][j]=data[str(i)][j-1]
                except:
                    continue
                
                
    data.to_csv(path,header=True,index=False)#csv로 다시 저장
     


#두점 사이 거리 구하기
def length(x1,y1,x2,y2):
    return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))



#총 이동한 픽셀 거리 반환
def distance(path,part):
    total_distance=0#총길이
    
    x,y=0,0#현재 좌표
    next_x,next_y= 0,0#다음 좌표
    
    data = pd.read_csv(path)
    data=data[part]#부위 데이터만 추출
    
    #처음 좌표
    x,y=data[0].split(", ")
    x,y=int(x),int(y)

    for i in range(len(data)-1):
        if data[i] != data[i+1]:#위치가 변했을 경우
            next_x,next_y=data[i+1].split(", ")#좌표 저장
            next_x,next_y=int(next_x),int(next_y)
            total_distance+=length(x,y,next_x,next_y)
            x,y=next_x,next_y
                  
    return total_distance    



#csv 파일 경로와 3부위를 입력받아 angle을 구하는 함수-맞는 알고리즘인지 코드검수 필요
def angle(path,first,second,third):
    data = pd.read_csv(path)
    row,column=data.shape
    angle_list=[]
    
    #원하는 3지점 데이터 받아오기
    first_list=data[str(first)]
    second_list=data[str(second)]
    third_list=data[str(third)]
    
    for i in range(int(row)):
        #프레임별 위치 데이터 불러오기
        f_x,f_y=map(int,(first_list[i].split(",")))
        s_x,s_y=map(int,(second_list[i].split(",")))
        t_x,t_y=map(int,(third_list[i].split(",")))
    
        s_to_f=(f_x-s_x,f_y-s_y)#second-first
        s_to_t=(t_x-s_x,t_y-s_y)#second-third
        
        dot=s_to_f[0]*s_to_t[0]+s_to_f[1]*s_to_t[1]
        det=s_to_f[0]*s_to_t[1]-s_to_f[1]*s_to_t[0]
        
        theta=np.rad2deg(np.arctan2(det, dot))
        angle_list.append(theta)


    return angle_list

#전프레임에서 다음프레임 부위 이동방향 구하는 함수
def direction(path,User_classification):
    data = pd.read_csv(path)
    row_count=len(data) #프레임수
    df_new=pd.DataFrame()
    
    for i in range(0,15):
        df=pd.DataFrame(columns=["id",i])
        for j in range(0, row_count-1):
            
            #처음 좌표
            data_1=data.iat[j,i]
            x1,y1=data_1.split(", ")
            x1,y1=int(x1),int(y1)
    
            data_2=data.iat[j+1,i]
            x2,y2=data_2.split(", ")
            x2,y2=int(x2),int(y2)

            a=math.atan2(-(y2-y1),x2-x1)*(180/math.pi) # 방위각 계산, cv좌표계 -> y축변환
            
            if x1==x2 and y1==y2:
                direct="＃" #움직임 없음
            elif 0<=a<=45: 
                direct=1 # →에서 ↗까지
            elif 45<a<=90: 
                direct=2 # ↗에서 ↑까지
            elif 90<a<=135:
                direct=3 # ↑에서 ↖까지
            elif 135<a<=180:
                direct=4 # ↖에서 ←까지
            elif -180<a<=-135: 
                direct=5 # ←에서 ↙까지
            elif -135<a<=-90: 
                direct=6 # ↙에서 ↓까지
            elif -90<a<=-45: 
                direct=7 # ↓에서 ↘까지
            elif -45<a<0:
                direct=8 #↘에서 →까지
        
            df= df.append(pd.DataFrame([[j,direct]], columns=["id",i]), ignore_index=True)
        df_new=df_new.append(df[i])
    
    df_new=df_new.transpose()
    if User_classification=='trainer':
        df_new.to_csv("./trainer/direct.csv", index = False)
    else:
        df_new.to_csv("./user/direct.csv", index = False)
    return df_new    
    













