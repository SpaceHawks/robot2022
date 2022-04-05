import serial

class Motor:
    power = 0

    def __init__(self):
        pass

    def __str__(self):
        pass


class DriveTrain:

    def __init__(self):
        self.frontRight = Motor()
        self.frontLeft = Motor()
        self.backRight = Motor()
        self.backLeft = Motor()

    def driveForward(self, power):
        self.setMotorPowers(power, power, power, power)

    def tankDrive(self, leftPower, rightPower):
        self.setMotorPowers(rightPower, leftPower, rightPower, leftPower)

    def setMotorPowers(self, FR, FL, BR, BL):
        self.frontRight.power = FR
        self.frontLeft.power = FL
        self.backRight.power = BR
        self.backLeft.power = BL

    def stopRobot(self):
        self.setMotorPowers(0,0,0,0)

    def __str__(self):
        return f"Motor Powers: FR:{self.frontRight.power}, FL:{self.frontLeft.power}, BR:{self.backRight.power}, BL:{self.backLeft.power}"

    def __repr__(self):
        return str(self)
