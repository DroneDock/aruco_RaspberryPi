"""
Import this to plot all 3 angles when running the IMU
ZA
"""
import matplotlib.pyplot as plt

class graph(object):
    def __init__(self):
        self.yaw = []
        self.pitch = []
        self.roll = []
        self.time = []

        
    def plot_graph(self,timestamps:float, yaw_values:float, roll_values:float, pitch_values:float):
        self.yaw.append(yaw_values)
        self.pitch.append(pitch_values)
        self.roll.append(roll_values)
        self.time.append(timestamps)
    #     Plotting all 3 graphs together
    #     plt.clf()
    #     plt.plot(self.time, self.yaw, label='Yaw', color='r')
    #     plt.plot(self.time, self.roll, label='Roll', color='g')
    #     plt.plot(self.time, self.pitch, label='Pitch', color='b')
    #     plt.legend()
    #     plt.xlabel('Time')
    #     plt.ylabel('Angle (degrees)')
    #     plt.title('IMU Euler Angles')
    #     plt.pause(0.001)
    #     plt.savefig('Reach_Angles.png')
            # Plot and save Yaw angle
        plt.clf()
        plt.plot(self.time[2:], self.yaw[2:], label='Yaw', color='r')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Angle (degrees)')
        plt.title('Yaw Angle')
        plt.savefig('Yaw_Angle3.png')
        
        # Plot and save Roll angle
        plt.clf()
        plt.plot(self.time[2:], self.roll[2:], label='Roll', color='g')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Angle (degrees)')
        plt.title('Roll Angle')
        plt.savefig('Roll_Angle3.png')

        # Plot and save Pitch angle
        plt.clf()
        plt.plot(self.time[2:], self.pitch[2:], label='Pitch', color='b')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Angle (degrees)')
        plt.title('Pitch Angle')
        plt.savefig('Pitch_Angle3.png')

    def graph_singular(self,timestamps:float, roll_values:float):
        self.roll.append(roll_values)
        self.time.append(timestamps)
        plt.clf()
        plt.plot(self.time[2:], self.roll[2:], label='Roll', color='g')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Angle (degrees)')
        plt.title('Roll Angle')
        plt.savefig('Roll_limit.png')