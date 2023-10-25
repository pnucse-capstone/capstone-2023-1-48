from enum import Enum

class Label(Enum):
    COLD = 0
    HOT = 1
    WARM = 2

# 초기 비율이 HOT:WARM:COLD = 3:7:2 정도 이므로, SSD의 BLOCK LABEL 비율도 동일하게 가져간다.
