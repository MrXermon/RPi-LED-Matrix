# -*- coding: utf-8 -*-
def cleanMessage(message):
        # Replace smileys
        message = message.replace('☺', chr(1))
        message = message.replace('☻', chr(2))
        message = message.replace('♥', chr(3))
        message = message.replace('♦', chr(4))
        message = message.replace('♣', chr(5))
        message = message.replace('♠', chr(6))
        message = message.replace('♪', chr(13))
        message = message.replace('♫', chr(14))
        message = message.replace('►', chr(16))
        message = message.replace('◄', chr(17))
        message = message.replace('▲', chr(30))
        message = message.replace('▼', chr(31))
        message = message.replace('\n', ' ')

        # Replace german special characters
        message = message.replace('ß', chr(225))
        message = message.replace('Ä', chr(142))
        message = message.replace('Ü', chr(154))
        message = message.replace('Ö', chr(153))
        message = message.replace('ä', chr(132))
        message = message.replace('ü', chr(129))
        message = message.replace('ö', chr(148))
        return message
