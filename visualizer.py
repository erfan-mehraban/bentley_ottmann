import matplotlib.pyplot as plt

class Visualizer:

    def __init__(self):
        self.segments = []
        self.points = []

    def add_segment(self, p1, p2):
        self.segments.append([p1[0], p2[0]])
        self.segments.append([p1[1], p2[1]])
        self.segments.append('r')

    def add_point(self, p):
        self.points.append(p)

    def show(self):
        plt.plot(*self.segments)
        plt.plot([p[0] for p in self.points], [p[1] for p in self.points] , '.')
        plt.show()

