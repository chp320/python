import enum
from collections import namedtuple

#########################################
# 선수는 흑(black)과 백(white) 으로 구분됨
# 선수가 착수(돌을 둠) 후 other() 호출하여 색을 바꿈(선수 교체)
#########################################
class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

#########################################
# 바둑판 상 돌의 좌표는 '튜플'을 사용해서 표현함
# 돌을 두는 지점은 '착점'으로 해당 점(POINT)의 이웃(neighbor)의 활로를 찾는다.
# ㄴ 확인 가능한 이웃은 왼쪽,오른쪽,위,아래 4곳 이다.
#########################################
class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]