from mecademic import MecaRobot


MECA_IP = "192.168.0.100"
MECA_PORT = 10000

robot = MecaRobot(MECA_IP, MECA_PORT)

home = [0.0014, 0.0, 0.0, 0.0, 0.0, 0.0]
away1 = [29.868040, 27.122770, -21.334730, -28.940260, 49.864250, 39.713300]
away2 = [-29.868040, -27.122770, 21.334730, 28.940260, -49.864250, -39.713300]
away_var = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
robot.run('SetJointVel', 25, True)

robot.run('MoveJoints', home, True)
robot.run('MoveJoints', away1, True)
robot.run('MoveJoints', away2, True)
print("hello")

exit()

robot.run('MoveJoints', away2, True)

[a, b, c, d, e, f] = robot.get_joints()
print('sum of joints =', a + b + c + d + e + f)



var = 10

away_var = away2
away_var[0] = away_var[0]+ var
robot.run('MoveJoints', away_var, True)
