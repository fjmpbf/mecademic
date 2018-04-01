from mecademic import MecaRobot

MECA_IP = "192.168.0.100"
MECA_PORT = 10000

home = [0.0014, 0.0, 0.0, 0.0, 0.0, 0.0]
away1 = [30, 27.122770, -21.334730, -28.940260, 49.864250, 39.713300]
A1Pos = [15, 0.0, 0.0, 0.0, 0.0, 0.0]
MoveJoint_var = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

class RobotController():
    #Initial set up for homing procedure
    def __init__(self):
        self.mecarobot = MecaRobot(MECA_IP, MECA_PORT)
        self.mecarobot.run('set_joint_vel',25, True)

    #......................GUI commands


    # Moves robot to Home point using the Up push button
    def up(self):
        self.mecarobot.run('MoveJoints', home)

    # Moves robot to away1 point using the Down push button
    def down(self):
        self.mecarobot.run('MoveJoints', away1)

    # Reads joints values from robot
    def get_joints(self, t1, t2, t3, t4, t5, t6):
        self.mecarobot.run('GetJoints', [t1, t2, t3, t4, t5, t6])

    def connect_feedback(self, handler):
        self.mecarobot.monitor(handler)

    def connect_log(self, handler):
        self.mecarobot.log(handler)


    #......................MECADEMIC Motion commands
    # JOINTS
    def move_joints(self, t1, t2, t3, t4, t5, t6):
        self.mecarobot.run('MoveJoints', [t1, t2, t3, t4, t5, t6])

    def move_jointsDelta(self, t1, t2, t3, t4, t5, t6):
        self.mecarobot.run('MoveJointsDelta', [t1, t2, t3, t4, t5, t6])

    def set_joint_vel(self, AngSpeed):
        self.mecarobot.run('SetJointVel',AngSpeed)

    # LINEAR
    def move_lin(self, x, y, z, a, b, g):
        self.mecarobot.run('MoveLin', [x, y, z, a, b, g])

    def move_linearDelta(self, x, y, z, a, b, g):
        self.mecarobot.run('SetMoveLinDeltaRef', 0)
        self.mecarobot.run('MoveLinDelta', [x, y, z, a, b, g])

    def set_cart_lin_vel(self,LinSpeed):
        self.mecarobot.run('SetCartLinVel',LinSpeed)


    #......................MECADEMIC Request commands

    def pause_motion(self):
        self.mecarobot.run('PauseMotion')

    def resume_motion(self):
        self.mecarobot.run('ResumeMotion')

    def clear_motion(self):
        self.mecarobot.run('ClearMotion')

    def reseterror(self):
         self.mecarobot.run('ResetError')
