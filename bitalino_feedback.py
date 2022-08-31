import pygame
import random
from ndf_lsl import ndf_lsl
import numpy as np

WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)


class FeedbackCircle:
    def __init__(self):
        self.radius = int(HEIGHT/10)
        self.colour = (255, 0, 0)
        self.position = [int(WIDTH/2), int(HEIGHT/2)]
        self.step = int(HEIGHT/50)

    def move(self, emg_on):
        if emg_on == True:
            # If EMG activated, go up
            self.position[1] = self.position[1] - self.step
        else:
            # By default, go down
            self.position[1] = self.position[1] + self.step

        # Check if it has reached the bottom
        if(self.position[1] > HEIGHT-self.radius):
            self.position[1] = HEIGHT-self.radius

        # Check if it has reached the top
        if(self.position[1] < self.radius):
            self.position[1] = self.radius

    def draw(self, screen, emg_on):
        self.move(emg_on)
        pygame.draw.circle(screen, self.colour, self.position, self.radius)


def main():

    # Pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Create a feedback object (circle)
    fb = FeedbackCircle()

    # Setup LSL object and resolve incoming stream from Bitalino
    ndf = ndf_lsl(stream_name="OpenSignals")
    ndf.ndf_setup()

    while True:

        # By default, I set OpenSignas to send me the following channels, in this order:
        # 1: EMG1. 2: EMG2 (this is just an example, modify it accordingly)
        buffer = ndf.ndf_read()[1]
        ecg = buffer[:, 1] - buffer[:, 0]
        AvgAbsECG = np.max(np.abs(ecg))
        print("AvgVal = ", AvgAbsECG)
        if AvgAbsECG > 950:
            emg_on = True
        else:
            emg_on = False
        print("emg_on = ", emg_on)

        screen.fill(BACKGROUND)
        fb.draw(screen, emg_on)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()