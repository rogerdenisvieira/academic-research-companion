import json
import logging
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ChatterBotCorpusTrainer

CORPUS_DIR = './data/corpus'
THRESHOLD_CONFIDENCE = 0.5
logging.basicConfig(level=logging.INFO)


class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)
    trainer = ChatterBotCorpusTrainer(chatterbot)
    #trainer = UbuntuCorpusTrainer(chatterbot)
    trainer.train(CORPUS_DIR)




    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        print(input_data)

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)


        response = self.chatterbot.get_response(input_data)

        if float(response.confidence > THRESHOLD_CONFIDENCE):
            response_data = response.serialize()
        else:
            response_data = {'text': [
                'I did not understand, please be more specific.'
                ]}
                    
        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })
