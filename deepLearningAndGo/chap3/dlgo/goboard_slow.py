import copy
from dlgo.gotypes import Player

#########################################
# 기사(Player)의 행동을 처리하는 클래스
# - 수행 가능한 행동은 [돌 놓기(is_play), 차례 넘기기(is_pass), 대국 포기(is_resign)] 3가지 이다.
#########################################
# Move 생성자를 직접 호출하지 않고,
# Move의 인스턴스를 생성하는 Move.play(), Move.pass_turn(), Move.resign()을 호출
class Move():
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert(point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign
    
    # 바둑판에 돌을 놓음
    @classmethod
    def play(cls, point):
        return Move(point=point)
    
    # 차례를 넘김
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    # 현재 대국을 포기
    @classmethod
    def resign(cls):
        return Move(is_resign=True)
    

#########################################
# 1. 돌을 놓을 때 '활로'가 남아 있는 이웃이 있는지 살펴 본다.
# 2. 이웃의 이웃 중에도 '활로'가 남은 경우가 있는지 확인한다.
# 3. 이웃의 이웃의 이웃도 조사하고, 그 이상도 살펴봐야 한다.
# => 위와 같이 확인하게 되면 복잡도가 증가한다.
# '같은 색' 돌이 연결된 그룹과 이 그룹의 '활로'를 찾아본다.
# ㄴ 같은 색 돌이 연결된 그룹을 '이음수' 혹은 '이음' 이라고 함
#########################################

#########################################
# 정의: '이음'을 구현
# 1. 같은 색의 이음을 연결
# 2. 상대방 '색' 돌의 근접한 이음의 활로 수를 낮춘다. (돌을 둔 경우)
# 3. 상대방 '색' 돌의 이음의 활로가 0이라면 이를 제거한다. => 돌을 둘 수 없게 함.
#########################################
class GoString():
    def __init__(self, color, stones, liberties) :
        self.color = color
        self.stones = stones
        self.liberties = set(liberties)
    
    # 주어진 이음의 활로를 제거 => 상대가 이 이음 옆에 돌을 두는 경우
    def remove_liberty(self, point):
        self.liberties.remove(point)
    
    # 주어진 이음의 활로를 추가 => 이 이음 근처의 집에서 상대방의 돌을 따내면 경우
    def add_liberty(self, point):
        self.liberties.add(point)
    
    # 양 선수의 '이음의 모든 돌'을 저장한 새 이음을 반환 => 착수 후 떨어져 있는 두 개의 그룹이 연결된 경우
    def merged_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones
        )
    
    # for 활로 확인
    @property
    def num_liberties(self):
        return len(self.liberties)
    
    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties
    