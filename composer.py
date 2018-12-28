import random

from visualizer import Visualizer
from bentley_ottmann import BentleyOttmann

MAX_X = 1000
MAX_Y = 1000

def generate_point():
    return (random.randint(0, MAX_X), random.randint(0, MAX_Y))

def generate_segments(n):
    for _ in range(n):
        s = generate_point()
        e = generate_point()
        if e[0] < s[0]:
            e, s = s, e
        elif e[0]==s[0] and e[1] < s[1]:
            e, s = s, e
        yield (s, e)

def random_segment_test():
    v = Visualizer()
    segments = list(generate_segments(5))
    bo = BentleyOttmann(segments)
    print(segments)
    for s in segments:
        v.add_segment(s[0], s[1])
    # v.show()
    bo.run()
    for p in bo.result:
        v.add_point(p)
    v.show()


if __name__ == "__main__":
    random_segment_test()