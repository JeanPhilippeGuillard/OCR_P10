from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce
from config import (authoringKey, authoringEndpoint, predictionEndpoint)

import json, time

# <AuthoringSortModelObject>
def get_child_id(model, childName):


    theseChildren = next(filter((lambda child: child.name == childName), model.children))
    
    ChildId = theseChildren.id
    print("ChildId :", ChildId)

    return ChildId


def get_grandchild_id(model, childName, grandChildName):
    
    theseChildren = next(filter((lambda child: child.name == childName), model.children))
    theseGrandchildren = next(filter((lambda child: child.name == grandChildName), theseChildren.children))

    grandChildId = theseGrandchildren.id

    return grandChildId

def load_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)


def quickstart():

    # Set variables ----------------------------------------------------

    appName = "BookFlight-v5-SDK"
    versionId = "0.1"

    # Authenticate client------------------------------------------------

    client = LUISAuthoringClient(authoringEndpoint, CognitiveServicesCredentials(authoringKey))

    # Create LUIS application -------------------------------------------

    # define app basics
    appDefinition = {
        "name": appName,
        "initial_version_id": versionId,
        "culture": "en-us"
    }
    
    # Create app
    app_id = client.apps.add(appDefinition)
    
    # get app id - necessary for all other changes
    print(f"Created LUIS app with id {app_id}")

    # Create intention(s) ------------------------------------------------
    
    intentNames = ["BookFlight", "Confirm", "Greetings"]
    for intent in intentNames:
        client.model.add_intent(app_id, versionId, intent)

 
    # Create entity(ies) -------------------------------------------------

    # Add pre_built entity :

    client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=["money", "geographyV2", "datetimeV2"])


    # Create ML entity :
    mlEntityDefinition = [
            {
                "name": "From",
                "children": [
                    {"name": "Airport"}
                ]
            },
            {
                "name": "To",
                "children": [
                    {"name": "Airport"}
                ]
            },
            {"name": "Departure_date"},
            {"name": "Return_date"},
            {"name": "budget"}
        ]
    
    airport_entity = {"name": "Airport"}


    # Add ML entity to app

    #modelId = client.model.add_entity(app_id, versionId, name="From", children=airport_entity)
    from_entity = client.model.add_entity(app_id, versionId, name="From", children=[airport_entity] )
    to_entity = client.model.add_entity(app_id, versionId, name="To", children=[airport_entity])

    departure_date_id = client.model.add_entity(app_id, versionId, name="Departure_date")
    return_date_id = client.model.add_entity(app_id, versionId, name="Return_date")
    budget_id = client.model.add_entity(app_id, versionId, name="budget")
    
     
    # define phraselist - add phrases as significant vocabulary to app


    # Get entity and sub-entities for nested entities:
    from_object = client.model.get_entity(app_id, versionId, from_entity)
    to_object = client.model.get_entity(app_id, versionId, to_entity)

    from_airport_id = get_child_id(from_object, "Airport")
    to_airport_id = get_child_id(to_object, "Airport")

    """departure_fromId = get_grandchild_id(modelObject, "location", "departure_location")
    return_fromId = get_grandchild_id(modelObject, "location", "return_location")
    departure_date = get_grandchild_id(modelObject, "date", "departure_date")
    return_dateId = get_grandchild_id(modelObject, "date", "return_date")
    print("Liste des entités :", [child.name for child in modelObject.children])
    travelersId = get_child_id(modelObject, "travelers")"""
    
    """departure_date_id = departure_date_entity.id
    return_date_id = return_date_entity.id
    budget_id = budget_entity.id"""
    

    # Add model as feature to subentity model
    prebuiltFeatureRequiredDefinition = {"model_name" : "geographyV2", "is_required": True}
    client.features.add_entity_feature(app_id, versionId, from_airport_id, prebuiltFeatureRequiredDefinition)
    client.features.add_entity_feature(app_id, versionId, to_airport_id, prebuiltFeatureRequiredDefinition)
    prebuiltFeatureRequiredDefinition = {"model_name": "datetimeV2", "is_required": True}
    client.features.add_entity_feature(app_id, versionId, departure_date_id, prebuiltFeatureRequiredDefinition)
    client.features.add_entity_feature(app_id, versionId, return_date_id, prebuiltFeatureRequiredDefinition)
    prebuiltFeatureRequiredDefinition = {"model_name": "money", "is_required": True}
    client.features.add_entity_feature(app_id, versionId, budget_id, prebuiltFeatureRequiredDefinition)


    # Add phraselist as feature to subentity model
    
    # Add utterances examples to intents ----------------------------------------------

    # Define labeled examples :

    old_BookFlight_utterance = {
        "text": "Hello. Id'like to book a flight from Paris to New-York, leaving on Saturday, August 13, 2016 and returning on Tuesday, August 16, 2016. I have a budget of $3700. ",
        "intentName": intentNames[0],
        "entityLabels": [
                    {
                        "startCharIndex": 37,
                        "endCharIndex": 53,
                        "entityName": "location",
                        "children": [
                            {
                                "startCharIndex": 37,
                                "endCharIndex": 41,
                                "entityName": "departure_location"
                            },
                            {
                                "startCharIndex": 46,
                                "endCharIndex": 53,
                                "entityName": "return_location"
                            }]
                    },
                    {
                        "startCharIndex": 67,
                        "endCharIndex": 133,
                        "entityName": "date",
                        "children": [
                            {
                                "startCharIndex": 67,
                                "endCharIndex": 91,
                                "entityName": "departure_date"
                            },
                            {
                                "startCharIndex": 110,
                                "endCharIndex": 133,
                                "entityName": "return_date"
                            }]
                        },
                    {
                        "startCharIndex": 155,
                        "endCharIndex": 159,
                        "entityName": "budget"
                        }
                    ]
                }


    BookFlight_utterance = {
        "text": "I'd like to book a trip to Atlantis from Caprica on Saturday, August 13, 2016 for 8 adults. I have a tight budget of 1700.",
        "intent": "BookFlight",
        "entities": [
            {
                "entity": "To",
                "startPos": 27,
                "endPos": 35,
                "children": [
                    {
                        "entity": "Airport",
                        "startPos": 27,
                        "endPos": 35
                    }
                ]
            },
            {
                "entity": "From",
                "startPos": 41,
                "endPos": 48,
                "children": [
                    {
                        "entity": "Airport",
                        "startPos": 41,
                        "endPos": 48
                    }
                ]
            },
            {
                "entity": "Departure_date",
                "startPos": 52,
                "endPos": 77
            },
            {
                "entity": "budget",
                "startPos": 117,
                "endPos": 121
            }
        ]
    }

    BookFlight_utterance = {
        "text": "Hello. Id'like to book a flight from Paris to New-York, leaving on Saturday, August 13, 2016 and returning on Tuesday, August 16, 2016. I have a budget of $3700. ",
        "intentName": intentNames[0],
        "entityLabels": [
                    {
                        "startCharIndex": 37,
                        "endCharIndex": 41,
                        "entityName": "From",
                        "children": [
                            {
                                "startCharIndex": 37,
                                "endCharIndex": 41,
                                "entityName": "Airport"
                            }]
                    },
                    {
                        "startCharIndex": 46,
                        "endCharIndex": 53,
                        "entityName": "To",
                        "children": [
                            {
                                "startCharIndex": 46,
                                "endCharIndex": 53,
                                "entityName": "Airport"
                            }]
                    },
                    {
                        "startCharIndex": 67,
                        "endCharIndex": 91,
                        "entityName": "Departure date"
                    },
                    {
                        "startCharIndex": 110,
                        "endCharIndex": 139,
                        "entityName": "Return date"
                    },
                    {
                        "startCharIndex": 155,
                        "endCharIndex": 159,
                        "entityName": "budget"
                        }
                    ]
                }
    BookFlight_json_file = "../training_data/training_data_03.json"
    BookFlight_utterance = load_json(BookFlight_json_file)
    print("\nBookFlight_utterance : ", BookFlight_utterance)

    Confirm_utterance = {
        "text": "OK",
        "intentName": intentNames[1]
    }

    Greetings_utterance = {
        "text": "Hello",
        "intentName": intentNames[2]
    }

    # Add an example for the entity
    # Enable nested children to allow using multiple models with the same name
    # The "quantity" subentity and the phraselise could have the same exact name if this is set to True
    for utterance in BookFlight_utterance:
        print("\nutterance : ", utterance)
        client.examples.add(app_id, versionId, utterance, {"enableNestedChildren": True})
    client.examples.add(app_id, versionId, Confirm_utterance, {"enableNestedChildren": False})
    client.examples.add(app_id, versionId, Greetings_utterance, {"enableNestedChildren": False})

    # Train the model ---------------------------------------------------------

    client.train.train_version(app_id, versionId)
    waiting = True
    while waiting:
        info = client.train.get_status(app_id, versionId)

        # get_status returns a list of training statuses , one for each model. Loop through them and make sure all are done.
        waiting = any(map(lambda x: "Queued" == x.details.status or "InProgess" == x.details.status, info))
        if waiting :
            print("Waiting 10 seconds for training to complete")
            time.sleep(10)
        else:
            print("Trained")
            waiting = False
    
    # Publish the app ---------------------------------------------------------

    responseEndpointInfo = client.apps.publish(app_id, versionId, is_staging=False)
    print("Model published to Production slot")

    # Authenticate prediction runtime client ----------------------------------

    runtimeCredentials = CognitiveServicesCredentials(authoringKey) # for test only. For production, use prediction key
    clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)

    # Get a prediction from runtime --------------------------------------------

    # Production == slot name
    predictionRequest = {"query": "Hi. i'd like to fly from New-York to Las-Vegas on August 10, 2021"}

    predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
    print(f"Top intent : {predictionResponse.prediction.top_intent}")
    print(f"Sentiment : {predictionResponse.prediction.sentiment}")

    for intent in predictionResponse.prediction.intents:
        print(f"\t{json.dumps(intent)}")
    print(f"Entities : {predictionResponse.prediction.entities}")




quickstart()