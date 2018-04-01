from functools import partial
from design import Ui_MainWindow
from robot_controller import RobotController
from PyQt5.QtWidgets import (QLineEdit,QSlider,QTableWidgetItem)

MoveJoint_var = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
MoveLin_var = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

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
        self.sldAngSpeedValue.valueChanged.connect(self.joint_speed_slided)
        self.sldCartSpeedValue.valueChanged.connect(self.cart_speed_slided)
        self.pbReadCurrAng.clicked.connect(self.pbReadCurrAng_clicked)
        self.pbMoveNewAngVal.clicked.connect(self.pbMoveNewAngVal_clicked)
        self.pbReadCurrCart.clicked.connect(self.pbReadCurrCart_clicked)
        self.pbMoveNewCartVal.clicked.connect(self.pbMoveNewCartVal_clicked)

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
        self.move_joints(index, 1)

    def pbTheta_dec_clicked(self, index):
        self.move_joints(index, -1)

    # Read the actual position values
    def pbReadCurrAng_clicked(self):
        self.lEditAngle1.setText (self.lblAngle1.text())
        self.lEditAngle2.setText (self.lblAngle2.text())
        self.lEditAngle3.setText (self.lblAngle3.text())
        self.lEditAngle4.setText (self.lblAngle4.text())
        self.lEditAngle5.setText (self.lblAngle5.text())
        self.lEditAngle6.setText (self.lblAngle6.text())

    # Moves to the new values
    def pbMoveNewAngVal_clicked(self):
        MoveJoint_var[0] = float(self.lEditAngle1.text())
        MoveJoint_var[1] = float(self.lEditAngle2.text())
        MoveJoint_var[2] = float(self.lEditAngle3.text())
        MoveJoint_var[3] = float(self.lEditAngle4.text())
        MoveJoint_var[4] = float(self.lEditAngle5.text())
        MoveJoint_var[5] = float(self.lEditAngle6.text())
        self.robot_controller.move_joints(*MoveJoint_var)
        self.lEditAngle1.setText("0")
        self.lEditAngle2.setText("0")
        self.lEditAngle3.setText("0")
        self.lEditAngle4.setText("0")
        self.lEditAngle5.setText("0")
        self.lEditAngle6.setText("0")

    # Set speed value for joint motion
    def joint_speed_slided(self):
        AngSpeed = self.sldAngSpeedValue.value()
        self.robot_controller.set_joint_vel(int(AngSpeed))

    # Execute joint motion
    def move_joints(self, index, direction):
         angles = [0, 0, 0, 0, 0, 0]
         angles[index] = direction * self.sldAngIncDecValue.value()
         self.robot_controller.move_jointsDelta(*angles)

    #...............................................................................
    #
    #     CARTESIANS
    #
    # ...............................................................................


    def pbCart_inc_clicked(self, index):
        self.move_linear(index, 1)

    def pbCart_dec_clicked(self, index):
        self.move_linear(index, -1)


    # Set speed value for linear motions
    def cart_speed_slided(self):
        CartSpeed = self.sldCartSpeedValue.value()
        self.robot_controller.set_cart_lin_vel(CartSpeed)

    # Execute linear motion
    def move_linear(self, index, direction):
        coords = [0, 0, 0, 0, 0, 0]
        coords[index] = direction * self.sldCartIncDecValue.value()
        self.robot_controller.move_linearDelta(*coords)

    # Read the actual position values
    def pbReadCurrCart_clicked(self):
        self.lEditCart1.setText (self.lblCart1.text())
        self.lEditCart2.setText (self.lblCart2.text())
        self.lEditCart3.setText (self.lblCart3.text())
        self.lEditCart4.setText (self.lblCart4.text())
        self.lEditCart5.setText (self.lblCart5.text())
        self.lEditCart6.setText (self.lblCart6.text())

    # Moves to the new values
    def pbMoveNewCartVal_clicked(self):
        MoveLin_var[0] = float(self.lEditCart1.text())
        MoveLin_var[1] = float(self.lEditCart2.text())
        MoveLin_var[2] = float(self.lEditCart3.text())
        MoveLin_var[3] = float(self.lEditCart4.text())
        MoveLin_var[4] = float(self.lEditCart5.text())
        MoveLin_var[5] = float(self.lEditCart6.text())
        self.robot_controller.move_lin(*MoveLin_var)
        self.lEditCart1.setText("0")
        self.lEditCart2.setText("0")
        self.lEditCart3.setText("0")
        self.lEditCart4.setText("0")
        self.lEditCart5.setText("0")
        self.lEditCart6.setText("0")

        self.tableWidget.setColumnWidth(1,50)
        self.tableWidget.setColumnWidth(2,50)
        self.tableWidget.setColumnWidth(3,50)
        self.tableWidget.setColumnWidth(4,50)
        self.tableWidget.setColumnWidth(5,50)
        self.tableWidget.setColumnWidth(6,50)
        item = QTableWidgetItem()
        item.setText("100.000")
        self.tableWidget.setItem(3,1,item)

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
