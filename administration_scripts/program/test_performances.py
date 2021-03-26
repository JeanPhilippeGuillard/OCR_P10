from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce

import json, time


def predict():

    # Set variables ----------------------------------------------------

    authoringKey = "2246a01e45d447ceb6f9799e72a75504"
    authoringResourceName = "jpg-luis-trial-authoring"
    predictionResourceName = "jpg-luis-trial"
    app_id = "d00b7fd0-1145-45cc-9171-97ca64dbbf92" #FlightBooking-v1

    authoringEndpoint = f"https://{authoringResourceName}.cognitiveservices.azure.com/"
    predictionEndpoint = f"https://{predictionResourceName}.cognitiveservices.azure.com"



    # Authenticate prediction runtime client ----------------------------------

    runtimeCredentials = CognitiveServicesCredentials(authoringKey) # for test only. For production, use prediction key
    clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)

    # Get a prediction from runtime --------------------------------------------

    # Production == slot name
    predictionRequest = {"query": "Hi. i'd like to fly from New-York to Las-Vegas on August 10, 2021"}
    predictionRequest = {"query": "Go to London for 200$"}

    predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
    print(f"Top intent : {predictionResponse.prediction.top_intent}")
    print(f"Sentiment : {predictionResponse.prediction.sentiment}")

    for intent in predictionResponse.prediction.intents:
        print(f"\t{json.dumps(intent)}")
    print(f"Entities : {predictionResponse.prediction.entities}")




predict()