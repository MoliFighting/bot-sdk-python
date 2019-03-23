#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/1/3

"""
    desc:pass
"""
import os
import logging
import traceback
from dueros.Bot import Bot
from dueros.card.TextCard import TextCard
from dueros.card.ImageCard import ImageCard
from dueros.card.StandardCard import StandardCard
from dueros.samples.xichuangzhu.Poem import Poem
from dueros.directive.BaseDirective import BaseDirective
import json
import random

class Bot(Bot):
    def launchRequest(self):
        standardCard = self.get_one_poem_standardCard()
        return {
            'card': standardCard,
            'outputSpeech': '<speak> %s </speak>' % standardCard.data["content"]
        }

    def nextIntentRequest(self):
        standardCard = self.get_one_poem_standardCard()
        return {
            'card': standardCard,
            'outputSpeech': '<speak> %s </speak>' % standardCard.data["content"]
        }

    def previousIntentRequest(self):
        standardCard = self.get_one_poem_standardCard()
        return {
            'card': standardCard,
            'outputSpeech': '<speak> %s </speak>' % standardCard.data["content"]
        }

    def seemoreIntentRequest(self):
        title = ""
        try:
            anchorText = (self._request.data["context"]["Screen"]["card"]["anchorText"])
        except Exception as e:
            standardCard = self.get_one_poem_standardCard()
            return {
                'card': standardCard,
                'outputSpeech': '<speak> %s </speak>' % standardCard.data["content"]
            }
        base_directive = BaseDirective("Display.RenderSwanView")
        poem_see_more = ""
        try:
            poem_see_more = Poem.get_see_more(gushiwen_url=anchorText)
        except Exception as e:
            print (traceback.print_exc())
        if poem_see_more:
            logging.info('poem_see_more:' + json.dumps(poem_see_more))
            standardCard = self.get_one_poem_standardCard()
            standardCard.data["title"] = poem_see_more["chuzi"]
            standardCard.data["content"] = poem_see_more["text"] + "\n\n" + poem_see_more["yiwen"]
            standardCard.data["image"] = Poem.get_one_random_image()
            return {
                'card': standardCard,
                'outputSpeech': '<speak> %s </speak>' % (poem_see_more["text"])
            }
        else:
            return {
                'outputSpeech': '<speak> 抱歉， 未找到这首诗 </speak>'
            }

    def get_one_poem_standardCard(self):
        standardCard = StandardCard()
        one_poem_item = Poem.get_one_poem_item()
        standardCard.data["title"] = one_poem_item["chuzi"]
        standardCard.data["content"] = one_poem_item["mingju"]
        standardCard.data['anchorText'] = one_poem_item["url"]
        standardCard.data["image"] = Poem.get_one_random_image()
        return standardCard

    def __init__(self, data):
        super(Bot, self).__init__(data)

        self.add_launch_handler(self.launchRequest)

        self.add_intent_handler('ai.dueros.common.next_intent', self.nextIntentRequest)

        self.add_intent_handler('ai.dueros.common.previous_intent', self.previousIntentRequest)

        self.add_intent_handler('xichuangzhu----see_more_about_it', self.seemoreIntentRequest)
        

    pass


if __name__ == '__main__':
    pass
