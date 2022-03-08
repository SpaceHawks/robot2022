class ControllerReceiver:

    def update(self, cmds):  #
        """inputs a string of controller updates; (Ex. AxY, AXL00) and sends it to dictionary storing the controller values
            Button updates will always appear first, then control stick updates.  """
        pass

    def A(self):
        """Check if A button was pressed.
        Returns True if pressed, False if released"""
        pass

    def B(self):
        """Check if B button was pressed.
        Returns True if pressed, False if released"""
        pass

    def X(self):
        """Check if X button was pressed.
        Returns True if pressed, False if released"""
        pass

    def Y(self):
        """Check if Y button was pressed.
        Returns True if pressed, False if released"""
        pass

    def leftStickX(self):
        """Returns value of leftStick X from 0-99"""
        pass

    def leftStickY(self):
        """Returns value of leftStick Y from 0-99"""
        pass

    def rightStickX(self):
        """Returns value of leftStick Y from 0-99"""
        pass

    def rightStickY(self):
        """Returns value of leftStick Y from 0-99"""
        pass

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
    cmd = 'AXYL78l50r05' # A Pressed, X Pressed, Y Pressed, Left Stick Y 78, left stick x 50, right stick x 75
    controller = ControllerReceiver()
    controller.update(cmd)
    print(controller.controllerValues)
    print(controller.A())
