from functools import partial
from design import Ui_MainWindow
from robot_controller import RobotController
from PyQt5.QtWidgets import (QLineEdit,QSlider)

MoveJoint_var = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


class RobotApp(Ui_MainWindow):



    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.robot_controller = RobotController()
        self.robot_controller.connect_feedback(self.feedback_changed)
        self.robot_controller.connect_log(self.update_log)

        self.pbUp.clicked.connect(self.pbUp_clicked)
        self.pbDown.clicked.connect(self.pbDown_clicked)
        self.pbResetError.clicked.connect(self.pbResetError_clicked)
        self.pbPauseMotion.clicked.connect(self.pbPauseMotion_clicked)
        self.pbResumeMotion.clicked.connect(self.pbResumeMotion_clicked)
        self.pbClearMotion.clicked.connect(self.pbClearMotion_clicked)
        self.pbMove.clicked.connect(self.pbMove_clicked)
        self.sldAngSpeedValue.valueChanged.connect(self.joint_speed_slided)

        for i in range(0, 6):
            pbTheta_inc = getattr(self, f'pbTheta{i+1}_inc')
            pbTheta_dec = getattr(self, f'pbTheta{i+1}_dec')
            pbTheta_inc.clicked.connect(partial(self.pbTheta_inc_clicked, i))
            pbTheta_dec.clicked.connect(partial(self.pbTheta_dec_clicked, i))

        for i in range(0, 6):
            pbCart_inc = getattr(self, f'pbCart{i+1}_inc')
            pbCart_dec = getattr(self, f'pbCart{i+1}_dec')
            pbCart_inc.clicked.connect(partial(self.pbCart_inc_clicked, i))
            pbCart_dec.clicked.connect(partial(self.pbCart_dec_clicked, i))


    #...............................................................................
    #
    #     JOINTS
    #
    # ...............................................................................

    # Used to save joints values before they change
    def load_lEditAngle(self):
        MoveJoint_var[0] = float(self.lblAngle1.text())
        MoveJoint_var[1] = float(self.lblAngle2.text())
        MoveJoint_var[2] = float(self.lblAngle3.text())
        MoveJoint_var[3] = float(self.lblAngle4.text())
        MoveJoint_var[4] = float(self.lblAngle5.text())
        MoveJoint_var[5] = float(self.lblAngle6.text())

    def pbTheta_inc_clicked(self, index):
        print("inc", MoveJoint_var)
        self.move_joints(index, 1)

    def pbTheta_dec_clicked(self, index):
        print("dec", MoveJoint_var)
        self.move_joints(index, -1)


   # pbMove Takes the values of lEditAngle and executes a motion to those value
    #        uses MoveJoint_var array for calculations
    def pbMove_clicked(self):
        MoveJoint_var[0] = float(self.lEditAngle1.text())
        MoveJoint_var[1] = float(self.lEditAngle2.text())
        MoveJoint_var[2] = float(self.lEditAngle3.text())
        MoveJoint_var[3] = float(self.lEditAngle4.text())
        MoveJoint_var[4] = float(self.lEditAngle5.text())
        MoveJoint_var[5] = float(self.lEditAngle6.text())
        self.robot_controller.move(*MoveJoint_var)
        self.lEditAngle1.setText("0")
        self.lEditAngle2.setText("0")
        self.lEditAngle3.setText("0")
        self.lEditAngle4.setText("0")
        self.lEditAngle5.setText("0")
        self.lEditAngle6.setText("0")

    def move_joints(self, index, direction):
        print ("Jogging axis")
        angles = [0, 0, 0, 0, 0, 0]
        angles[index] = direction * self.sldAngIncDecValue.value()
        self.robot_controller.move_jointsDelta(*angles)


    def joint_speed_slided(self):
        AngSpeed = self.sldAngSpeedValue.value()
        self.robot_controller.SetJointVel(AngSpeed)

    #...............................................................................
    #
    #     CARTESIANS
    #
    # ...............................................................................


    def pbCart_inc_clicked(self, index):
        self.move_linear(index, 1)

    def pbCart_dec_clicked(self, index):
        self.move_linear(index, -1)

    def move_linear(self, index, direction):
        coords = [0, 0, 0, 0, 0, 0]
        coords[index] = direction * self.sldCartIncDecValue.value()
        self.robot_controller.move_linearDelta(*coords)






    #...............................................................................
    #
    #     BUTTONS
    #
    # ...............................................................................

    # Commands the def up
    def pbUp_clicked(self):
        self.robot_controller.up()

    # Commands the def down
    def pbDown_clicked(self):
        self.robot_controller.down()



    #...............................................................................
    #
    #     COMMANDS
    #
    # ...............................................................................

 #   def get_joints(self, t1, t2, t3, t4, t5, t6):
   #     return self.mecarobot.run('GetJoints', [t1, t2, t3, t4, t5, t6])

    def update_log(self, direction, message):
        if direction == 'in':
            self.textedit_log.insertHtml(f'<span>{message}</span><br>')
        else:
            self.textedit_log.insertHtml(f'<span style="color: gray; font-style: italic;">{message}</span><br>')


    def feedback_changed(self, code, values):
        if code == '3007':
            self.lblAngle1.setText(f'{values[0]:.3f}')
            self.lblAngle2.setText(f'{values[1]:.3f}')
            self.lblAngle3.setText(f'{values[2]:.3f}')
            self.lblAngle4.setText(f'{values[3]:.3f}')
            self.lblAngle5.setText(f'{values[4]:.3f}')
            self.lblAngle6.setText(f'{values[5]:.3f}')
            for i in range(0, 6):
                MoveJoint_var[i]=values[i]

        if code == '3010':
            self.lblCart1.setText(f'{values[0]:.3f}')
            self.lblCart2.setText(f'{values[1]:.3f}')
            self.lblCart3.setText(f'{values[2]:.3f}')
            self.lblCart4.setText(f'{values[3]:.3f}')
            self.lblCart5.setText(f'{values[4]:.3f}')
            self.lblCart6.setText(f'{values[5]:.3f}')

    def pbResetError_clicked(self):
        self.robot_controller.reseterror()

    def pbClearMotion_clicked(self):
        self.robot_controller.clear_motion()

    def pbPauseMotion_clicked(self):
            self.robot_controller.pause_motion()

    def pbResumeMotion_clicked(self):
            self.robot_controller.resume_motion()
