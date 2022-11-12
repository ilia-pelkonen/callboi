from mycroft import MycroftSkill, intent_handler, intent_file_handler
from adapt.intent import IntentBuilder
import RPi.GPIO as GPIO
import time
class Drink(MycroftSkill):
    def initialize(self):
        self.register_entity_file('quantity.entity')
        self.register_entity_file('type.entity')

    def convert(self, unit1, volume1):
        ret = float(volume1);
        if unit1.strip() in ['oz','ounce','ounces'] :
            ret = float(volume1)*29.5735;
        return round(ret);
        
    def __init__(self):
        MycroftSkill.__init__(self)
        

    @intent_file_handler('drink.intent')
    def handle_drink(self, message):
        GPIO.setmode(GPIO.BCM)
        # Relay 1
        GPIO.setup(21, GPIO.OUT)
        # Relay 2
        GPIO.setup(26, GPIO.OUT)
        try:
            chan_list = (21,26)
            GPIO.output(chan_list, GPIO.LOW) #Both on 
            time.sleep(1);
            GPIO.output(21, GPIO.HIGH);#first off
            time.sleep(5);
            GPIO.output(26, GPIO.HIGH);#second off
        finally:
            GPIO.cleanup()
        self.speak_dialog('drink')

    @intent_handler(IntentBuilder('Custom')
                              .require('Custom').require('Volume1').require('Unit1').require('Type1').optionally('Volume2').optionally('Unit2').optionally('Type2'))
    def handle_do_you_like(self, message):
        volume1 = message.data.get('Volume1')
        unit1 = message.data.get('Unit1')
        type1 = message.data.get('Type1')
        if volume1 is None:
             volume1 = 0
        if unit1 is None:
             unit1 = ''
        if type1 is None:
             type1 = ''
        #self.speak_dialog('Volume1 is '+volume1 + ', Unit1 is '+unit1 + ', Type1 is '+type1 ) 
             
        volume2 = message.data.get('Volume2')
        unit2 = message.data.get('Unit2')
        # type2 = message.data.get('Type2')
        if volume2 is None:
             volume2 = 0
        if unit2 is None:
             unit2 = ''
        # if type2 is None:
        #      type2 = ''
        #self.speak_dialog('Volume2 is '+volume2 + ', Unit2 is '+unit2) 

        boozeVolume = self.convert(unit1, volume1) if type1.strip() in ['vodka','booze','liquor','alcohol','alcoholic']  else  self.convert(unit2, volume2)
        juiceVolume = self.convert(unit2, volume2) if type1.strip() in ['vodka','booze','liquor','alcohol','alcoholic']  else  self.convert(unit1, volume1)

        if boozeVolume>100:
            self.speak_dialog('You ask too much of liquor, boozer'); 
            return
        if juiceVolume>250:
            self.speak_dialog('You ask too much'); 
            return

        #pouring
        GPIO.setmode(GPIO.BCM)
        try:
            if boozeVolume:
                # Relay 1
                GPIO.setup(21, GPIO.OUT)
                GPIO.output(21, GPIO.LOW) #First on
                time.sleep(0.04*boozeVolume); #100 mls in 4 seconds
                GPIO.output(21, GPIO.HIGH);#first off

            if juiceVolume:
                # Relay 2
                GPIO.setup(26, GPIO.OUT)
                GPIO.output(26, GPIO.LOW) #Second on
                time.sleep(0.04*juiceVolume);
                GPIO.output(26, GPIO.HIGH);#Second off
        finally:
            GPIO.cleanup()

        if boozeVolume and juiceVolume:
            self.speak_dialog('Here is your '+str(boozeVolume) + 'ml of liquor and '+str(juiceVolume)+' ml of juice'); 
        elif juiceVolume:
            self.speak_dialog('Here is your '+str(juiceVolume)+' ml of juice'); 
        elif boozeVolume:
            self.speak_dialog('Here is your '+str(boozeVolume)+ 'ml of liquor'); 
    # @intent_file_handler('customMix.intent')
    # def handle_customMix(self, message):
    #     quantity = message.data.get('quantity');
    #     type = message.data.get('type');
    #     type2 = message.data.get('type2');
    #     quantity2 = message.data.get('quantity2');

    #     if not quantity or not type:
    #         self.speak('I did not understand')
    #         return

    #     if quantity2 is None:
    #         quantity2 = ''
    #     if type2 is None:
    #         type2 = ''
    #     #self.log.debug("q1: %s, q2: %s", quantity, quantity2);

    #     # GPIO.setmode(GPIO.BCM)
    #     # # Relay 1
    #     # GPIO.setup(21, GPIO.OUT)
    #     # # Relay 2
    #     # GPIO.setup(26, GPIO.OUT)
    #     # try:
    #     #     chan_list = (21,26)
    #     #     GPIO.output(chan_list, GPIO.LOW) #Both on 
    #     #     time.sleep(1);
    #     #     GPIO.output(21, GPIO.HIGH);#first off
    #     #     time.sleep(5);
    #     #     GPIO.output(26, GPIO.HIGH);#second off
    #     # finally:
    #     #     GPIO.cleanup()
    #     self.speak('Here is '+quantity+" off1 "+type+ ",,, "+quantity2+" off2 "+type2);
    #     #self.speak_dialog('customMix')

    @intent_file_handler('doubledrink.intent')
    def handle_doubledrink(self, message):
        GPIO.setmode(GPIO.BCM)
        # Relay 1
        GPIO.setup(21, GPIO.OUT)
        # Relay 2
        GPIO.setup(26, GPIO.OUT)
        try:
            chan_list = (21,26)
            GPIO.output(chan_list, GPIO.LOW) #Both on 
            time.sleep(2);
            GPIO.output(21, GPIO.HIGH);#first off
            time.sleep(4);
            GPIO.output(26, GPIO.HIGH);#second off
        finally:
            GPIO.cleanup()
        self.speak_dialog('doubledrink')

    @intent_file_handler('shot.intent')
    def handle_shot(self, message):
        GPIO.setmode(GPIO.BCM)
        # Relay 1
        GPIO.setup(21, GPIO.OUT)
        try:
            GPIO.output(21, GPIO.LOW) #first on 
            time.sleep(1);
            GPIO.output(21, GPIO.HIGH);#first off           
        finally:
            GPIO.cleanup()
        self.speak_dialog('shot')

    @intent_file_handler('doubleshot.intent')
    def handle_doubleshot(self, message):
        GPIO.setmode(GPIO.BCM)
        # Relay 1
        GPIO.setup(21, GPIO.OUT)
        try:
            GPIO.output(21, GPIO.LOW) #first on 
            time.sleep(2);
            GPIO.output(21, GPIO.HIGH);#first off           
        finally:
            GPIO.cleanup()
        self.speak_dialog('doubleshot')


    @intent_file_handler('juice.intent')
    def handle_juice(self, message):
        GPIO.setmode(GPIO.BCM)
        # Relay 1
        GPIO.setup(26, GPIO.OUT)
        try:
            GPIO.output(26, GPIO.LOW) #second on
            time.sleep(6)
            GPIO.output(26, GPIO.HIGH) #second off
        finally:
            GPIO.cleanup()
        self.speak_dialog('juice')
    
    


def create_skill():
    return Drink()

