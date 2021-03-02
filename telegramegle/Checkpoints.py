class Checkpoint(object):
    autoMode = False
    messagesCount = 0
    strangerAge = 0
    strangerName = ''
    amIAskingForName = False
    informedUser = False

    def reset(self):
        self.messagesCount = 0
        self.strangerAge = 0
        self.strangerName = ''
        self.amIAskingForName = False
        self.informedUser = False
