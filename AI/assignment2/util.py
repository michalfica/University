import abc
import functools
import queue
import random
from typing import Tuple, FrozenSet, Iterable, Optional, List, Set, Callable, Dict, Generic, TypeVar, Sequence, Any

T = TypeVar('T')

# 2D matrix


def init_random_matrix(rows, cols):
    return [[random.randint(0, 1) for _ in range(len(cols))] for _ in range(len(rows))]


def get_column(i, matrix):
    return [matrix[j][i] for j in range(len(matrix))]


def get_columns(matrix):
    return [get_column(i, matrix) for i in range(len(matrix[0]))]


# sequence
def neg_kth(seq: Iterable[int], index: int) -> Iterable[int]:
    return (int(not x) if index == i else x
            for i, x in enumerate(seq))


# funcs
def memo(f):
    m = {}

    @functools.wraps(f)
    def aux(*args):
        if args not in m:
            m[args] = f(*args)
        return m[args]

    return aux


# data structures
class PQueue(Generic[T]):
    """
    Hides priority of queue.PriorityQueue as optional parameter
    Elements of equal priority in FIFO order
    """

    def __init__(self) -> None:
        self.cnt = 0
        self.q = queue.PriorityQueue()
        self.q

    def push(self, item: T, priority: Any=1) -> None:
        self.q.put((priority, self.cnt, item))
        # print('push:', priority)
        self.cnt += 1

    def pop(self) -> T:
        _, _, item = self.q.get()
        # print('_____', item)
        return item


Out = TypeVar('Out')
TState = TypeVar('TState')


class SeekerGrid(abc.ABC, Generic[TState, Out]):
    moves = {'U': (-1, 0),
             'D': (1, 0),
             'L': (0, -1),
             'R': (0, 1), }
    map: List
    memo: Dict[TState, Out]
    fst: TState
    default: Out

    def _print(self, state):
        for i, row in enumerate(self.map):
            for j, c in enumerate(row):
                print('S' if (i, j) in state else c, end='')
            print()

    def search(self, p: Callable[[TState], float], **kwargs) -> Out:
        """finds shortest sequence of moves to finish state, using cost function p"""
        q: PQueue[TState] = PQueue()
        self.memo = {}
        self.memo[self.fst] = self.default
        q.push(self.fst, p(self.fst))
        while q:
            state = q.pop()
            # self._print(state)
            if self.is_end(state):
                return self.memo[state]
            for moves, next_state in self.next_states(state):
                if next_state not in self.memo:
                    self.memo[next_state] = moves
                    q.push(next_state, p(next_state))
        raise RuntimeError('Found nothing!')

    @abc.abstractmethod
    def is_end(self, state: TState) -> bool:
        pass

    @abc.abstractmethod
    def next_states(self, state: TState) -> Iterable[Tuple[Out, TState]]:
        pass

    def search_bfs(self, **kwargs) -> Out:
        return self.search(lambda _: 0, **kwargs)

    def search_astar(self, **kwargs) -> Out:
        return self.search(self.f, **kwargs)

    @abc.abstractmethod
    def f(self, state: TState) -> float:
        pass

    @abc.abstractmethod
    def h(self, state: TState) -> float:
        pass


# heuristics
class Heuristics:
    @staticmethod
    def manhattan(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def euclidean(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        x = abs(pos1[0] - pos2[0])
        y = abs(pos1[1] - pos2[1])
        return (x * x + y * y) ** 0.5
