import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        super().__init__()

    def plot(self, data, distance):
        x = range(distance) 
        plt.plot(x, data[:distance]) 
        plt.xlabel('Distance')
        plt.ylabel('Speed')
        plt.gca().invert_yaxis()
        plt.title('Plot of Speed vs Distance')
        plt.show()
        input('Continue?')
