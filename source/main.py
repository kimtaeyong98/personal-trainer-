import get_video_csv
import compare

#main
#get_video_csv.get_video("스쿼트","user")#user 스켈레톤 동영상과 csv 얻기
#get_video_csv.get_video("스쿼트","trainer")#trainer 스켈레톤 동영상과 csv 얻기

#csv 경로
trainer_csv_path='./trainer/trainer_output.csv'
user_csv_path='./user/user_output.csv'


#0,0 체크
compare.check(trainer_csv_path)
compare.check(user_csv_path)


#이동한 거리(머리)
distance_trainer_head=compare.distance(trainer_csv_path,str(0))
distance_user_head=compare.distance(user_csv_path,str(0))
print(distance_trainer_head)
print(distance_user_head)

#각도(왼쪽 무릎)
trainer_angle=compare.angle(trainer_csv_path,8,9,10)
print(trainer_angle)

