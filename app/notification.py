class Notification:

    def __init__(self, title, message):
        self.title = title
        self.message = message


class BreakNotification(Notification):

    def __init__(self):
        super().__init__('Break', 'Take a break!')
