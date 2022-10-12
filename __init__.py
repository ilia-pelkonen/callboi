from mycroft import MycroftSkill, intent_file_handler


class Drink(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('drink.intent')
    def handle_drink(self, message):
        self.speak_dialog('drink')


def create_skill():
    return Drink()

