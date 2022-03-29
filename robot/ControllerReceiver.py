class ControllerReceiver:
    buttonCommandReference = {
        # Uppercase letters means button was pressed, #Lowercase letters means button was released
        'A': True,
        'B': True,
        'X': True,
        'Y': True,
        'a': False,
        'b': False,
        'x': False,
        'y': False
    }

    controllerStickCommandReference = {
        'L': 'LX',
        'l': 'LY',
        'R': 'RX',
        'r': 'RY'
    }

    controllerValues = {  # Dictionary to stores all the values for the controller
        'A': False,
        'B': False,
        'X': False,
        'Y': False,
        'LX': 0,
        'LY': 0,
        'RX': 0,
        'RY': 0
    }

    # A = 'A'
    # B = 'B'
    # X = 'X'
    # Y = 'Y'
    # LeftStickX = 'LX'
    # RightStickX = 'RX'
    # LeftStickY = 'LY'
    # RightStickY = 'RY'

    def update(self, cmds):  #
        """inputs a string of controller updates; (Ex. AxY, AXL00) and sends it to dictionary storing the controller values
            Button updates will always appear first, then control stick updates.  """

        #
        # check if the next command is a button and if there are any commands left
        # all button commands are True (pressed) or False (released)
        while len(cmds) != 0 and self.buttonCommandReference.get(cmds[0]) is not None:
            buttonCommand = self.buttonCommandReference.get(cmds[0])  # True or False
            # print('button commond: ' + str(buttonCommand))
            self.controllerValues[cmds[0].capitalize()] = buttonCommand  # sets

            cmds = cmds[1:len(cmds)]  # remove the first command
            # print(f'cmds: {cmds}')

        print(f'control stick {cmds}')

        # Now we move onto control stick commands/ values on the control stick that require a numerical value
        while len(cmds) != 0:
            print(cmds)
            controlStick = self.controllerStickCommandReference.get(cmds[0])
            if cmds[1] == '-':  # invert all numbers to make that shit work
                stickValue = int(cmds[1:4])
                self.controllerValues[controlStick] = stickValue * -1
                cmds = cmds[4:len(cmds)]
            else:  # positive number
                stickValue = int(cmds[1:3])
                self.controllerValues[controlStick] = stickValue * -1
                cmds = cmds[3:len(cmds)]

    def A(self):
        """Check if A button was pressed.
        Returns True if pressed, False if released"""
        return self.controllerValues['A']

    def B(self):
        """Check if B button was pressed.
        Returns True if pressed, False if released"""
        return self.controllerValues['B']

    def X(self):
        """Check if X button was pressed.
        Returns True if pressed, False if released"""
        return self.controllerValues['X']

    def Y(self):
        """Check if Y button was pressed.
        Returns True if pressed, False if released"""
        return self.controllerValues['Y']

    def leftStickX(self):
        """Returns value of leftStick X from 0-99"""
        return self.controllerValues['LX']

    def leftStickY(self):
        """Returns value of leftStick Y from 0-99"""
        return self.controllerValues['LY']

    def rightStickX(self):
        """Returns value of leftStick Y from 0-99"""
        return self.controllerValues['RX']

    def rightStickY(self):
        """Returns value of leftStick Y from 0-99"""
        return self.controllerValues['RY']

    def __str__(self):
        thing = ''
        for k, v in self.controllerValues.items():
            thing += str(k) + ': ' + str(v) + ', ' \
                                              ''
        return thing

    def __repr__(self):
        return str(self)

# test this class with a test command
if __name__ == '__main__':
    cmd = 'AXYL78l50r05'
    controller = ControllerReceiver()
    controller.update(cmd)
    print(controller.controllerValues)
    print(controller.A())
