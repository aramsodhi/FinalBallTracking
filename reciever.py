import sys
import time
from networktables import NetworkTables

NetworkTables.initialize()
print("is server: " + str(NetworkTables.isServer()))
print("is connected: " + str(NetworkTables.isConnected()))

sd = NetworkTables.getTable("SmartDashboard")

while True:
    ball_x = sd.getNumber("ball_x", 0)
    ball_y = sd.getNumber("ball_y", 0)
    ball_on_screen = sd.getBoolean("ball_on_screen", False)
    
    print("ball_x: " + str(ball_x) + ", ball_y: " + str(ball_y) + ", ball_on_screen: " + str(ball_on_screen))
    
    time.sleep(0.1)