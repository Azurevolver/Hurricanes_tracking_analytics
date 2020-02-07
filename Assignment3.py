"""
Q1
variable: start, end, seg_dist, seg_time, speed
start = []
end = []
seg_dist = []
seg_time = []
start = last_end
if start == none, continue
end = current lat & lon(convert to value) -->function
total_dist = sum(seg_dist)
output file1
Q2
find_max_speed()
find_mean_speed()
output file2

Q3
variable: storm
storm = {}
for each row:
    calculate dist = distance btw storm eye & location
    if dist <= 5 and wind >=64 append storm ID to storm
    算location象限: 與颱風眼經緯度相減
    elif dist <= location象限的暴風半徑 (判斷是否落在該象限的風暴半徑內) append storm ID to storm
"""