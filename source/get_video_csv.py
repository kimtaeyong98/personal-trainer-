from scipy.spatial import distance as dist
import numpy as np
import pandas as pd
import progressbar
import cv2

#운동 종류 , 유저(사용자인지,트레이너인지)를 입력받아 스켈레톤 동영상을 생성하고 좌표를 csv로 저장
def get_video(exercise_Type, User_classification):
    
    protoFile = "./model/pose_deploy_linevec.prototxt"
    weightsFile = "./model/pose_iter_160000.caffemodel"
    
    if User_classification=="trainer":
        video_path = './video/trainer.mp4'
        out_path = './trainer/trainer_output.mp4'#결과 파일
        csv_path = './trainer/trainer_output.csv'#결과 파일 csv
    else:
        video_path = './video/user.mp4'
        out_path = './user/user_output.mp4'#결과 파일
        csv_path = './user/user_output.csv'#결과 파일 csv

    

    # 모델과 가중치 불러오기
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    #비디오 정보 저장
    cap = cv2.VideoCapture(video_path)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    ok, frame = cap.read()
    (frameHeight, frameWidth) = frame.shape[:2]
    h = frameHeight
    w = frameWidth

    # 모델에 입력을 크기 
    inHeight = h
    inWidth = w


    # 아웃풋(스켈레톤 동영상 설정)
    output = cv2.VideoWriter(out_path, 0, fps, (w, h))

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    writer = None
    (f_h, f_w) = (h, w)
    zeros = None

    data = []
    previous_x, previous_y = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    # 15개의 부위
    pairs = [[0,1], # 머리
            [1,2],[1,5], # 어깨
            [2,3],[3,4],[5,6],[6,7], # 팔
            [1,14],[14,11],[14,8], # 엉덩이
            [8,9],[9,10],[11,12],[12,13]] # 다리

    # 임계값
    thresh = 0.1

    #점,선 색
    circle_color, line_color = (0,255,255), (0,255,0)


    # 진행률 표시
    widgets = ["비디오 변환 진행률: ", progressbar.Percentage(), " ",
            progressbar.Bar(), " ", progressbar.ETA()]
    pbar = progressbar.ProgressBar(maxval = n_frames,
                                widgets=widgets).start()
    p = 0


    #관절 움직임 저장 리스트
    frame_xy=[[0],[1],[2],[3],[4],[5],
            [6],[7],[8],[9],[10],[11],
            [12],[13],[14]]

    # 시작
    while True:
        ok, frame = cap.read()
        if ok != True:
            break
        
        frame = cv2.resize(frame, (w, h), cv2.INTER_AREA)    
        frame_copy = np.copy(frame)
        
        # 네트워크 전처리
        inpBlob = cv2.dnn.blobFromImage(frame_copy, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
        net.setInput(inpBlob)
        output = net.forward()
        H = output.shape[2]
        W = output.shape[3]
        
        points = []
        x_data, y_data = [], []
        
        # 프레임별 데이터 저장 및 반복
        for i in range(15):
            probMap = output[0, i, :, :]
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
            x = (w * point[0]) / W
            y = (h * point[1]) / H
            
            
            if prob > thresh:
                points.append((int(x), int(y)))
                x_data.append(x)
                y_data.append(y)
            else :
                points.append((0, 0))
                x_data.append(previous_x[i])
                y_data.append(previous_y[i])
        
        for i in range(len(points)):
            cv2.circle(frame_copy, (points[i][0], points[i][1]), 5, circle_color, -1) 
            cv2.putText(frame_copy, str(i), (points[i][0], points[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1, lineType=cv2.LINE_AA)

            frame_xy[i].append((points[i][0], points[i][1]))
            #print(i," ",points[i][0], points[i][1],'',end='')
        
        #print() 
        for pair in pairs:
            partA = pair[0]
            partB = pair[1]
            cv2.line(frame_copy, points[partA], points[partB], line_color, 1, lineType=cv2.LINE_AA)
        
        if writer is None:
            writer = cv2.VideoWriter(out_path, fourcc, fps,
                                    (f_w, f_h), True)
            zeros = np.zeros((f_h, f_w), dtype="uint8")
        writer.write(cv2.resize(frame_copy,(f_w, f_h)))
        
        cv2.imshow('frame' ,frame_copy)
        
        data.append(x_data +y_data)
        previous_x, previous_y = x_data, y_data
        
        p += 1
        pbar.update(p)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # csv로 변환
    df = pd.DataFrame(frame_xy)
    df=df.transpose()
    df=df.drop(0)
    df.to_csv(csv_path, index = False)
    #print('저장완료')

    pbar.finish()
    cap.release()
    cv2.destroyAllWindows()