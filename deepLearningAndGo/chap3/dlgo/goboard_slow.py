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