import requests
import json
import string
from sklearn.metrics import precision_recall_fscore_support
from .config import (AUTHORING_KEY, APP_ID, APP_VERSION_ID, PREDICTION_ENDPOINT, SLOT_NAME)

connexion_string = f"{PREDICTION_ENDPOINT}luis/prediction/v3.0/apps/{APP_ID}/slots/{SLOT_NAME}/predict"
headers = {}

class performance_evaluator():
    def __init__(self, ground_truth, entities_name):
        self.ground_truth = ground_truth
        self.entities_name = entities_name

    def get_prediction(self, text):
        params = {
        'query': text,
        'timezoneOffset': '0',
        'verbose': 'true',
        'show-all-intents': 'true',
        'spellCheck': 'false',
        'staging': 'false',
        'subscription-key': AUTHORING_KEY
        }
        response = requests.get(connexion_string, headers=headers, params=params)
        return response.json()


    def get_ground_truth_entity(self, entities, entity_name):
        
        try:
            entity = entities[entity_name][0]["text"]
            entity = entity.translate(str.maketrans("", "", string.punctuation)) # remove punctuation
            return entity
        except KeyError:
            return ""


    def evaluate_intents_performance(self):
        # Get true intents
        text_to_predict = []
        intents_true = []
        intents_pred = []

        # Calculate predicted intents
        for turn in self.ground_truth:
            text = turn["text"]
            params = {
            'query': text,
            'timezoneOffset': '0',
            'verbose': 'true',
            'show-all-intents': 'true',
            'spellCheck': 'false',
            'staging': 'false',
            'subscription-key': AUTHORING_KEY
            }
            response = requests.get(connexion_string, headers=headers, params=params)
            response = response.json()
            try: # there may be some instances where responce["predicion"] doesn't exist
                intent_pred = response["prediction"]["topIntent"]
                intents_pred.append(intent_pred)
                # Keep intent_true evalauted after intent_pred to make sure that the 2 tables have the same length 
                intent_true = turn["intent"]
                intents_true.append(intent_true)
            except KeyError:
                pass

        precision, recall, fscore, _ = precision_recall_fscore_support(intents_true, intents_pred, average="micro")

        return precision, recall, fscore


    def build_dictionnaries(self, turn):

        ground_truth_dict = {}
        prediction_dict = {}
        
        
        # Initialize dictionnaries at each turn
        for entity in self.entities_name:
            ground_truth_dict[entity] = ""
            prediction_dict[entity] = ""

        # Get prediction
        text = turn["text"]
        prediction = self.get_prediction(text)

        # Build prediction dictionnary

        for i in turn["entities"]:
            entity_name = i["entity"]
            start = i["startPos"]
            end = i["endPos"]
            entity_value = turn["text"][start: end]
            entity_value = entity_value.translate(str.maketrans("", "", string.punctuation))
            ground_truth_dict[entity_name] = entity_value

        # Build prediction dictionnary

        try: # if there is no entity found, "$instance" key doesn't exist
            entities = prediction["prediction"]["entities"]["$instance"]

            prediction_dict["From"] = self.get_ground_truth_entity(entities, "From")
            prediction_dict["To"] = self.get_ground_truth_entity(entities, "To")
            prediction_dict["Departure date"] = self.get_ground_truth_entity(entities, "Departure date")
            prediction_dict["Return date"] = self.get_ground_truth_entity(entities, "Return date")
            prediction_dict["budget"] = self.get_ground_truth_entity(entities, "budget")
        except KeyError:
            pass

        return ground_truth_dict, prediction_dict


    def evaluate_entities_performance(self):
        y_true_dict = {}
        y_pred_dict = {}
        for entity in self.entities_name:
                y_true_dict[entity] = []
                y_pred_dict[entity] = []
        correct_preds = []

        for turn in self.ground_truth:
            ground_truth_dict, prediction_dict = self.build_dictionnaries(turn)

            for entity in y_true_dict:
                try:
                    y_true = ground_truth_dict[entity]
                except KeyError:
                    y_true = ""
                try:
                    y_pred = prediction_dict[entity]
                except KeyError:
                    y_pred = ""

                if y_true == y_pred:
                    if y_true != "":
                        y_true_class = 1
                        y_pred_class = 1
                    else:
                        y_true_class = 0
                        y_pred_class = 0
                else:
                    if y_true != "":
                        y_true_class = 1
                        y_pred_class = 0
                    else:
                        y_true_class = 0
                        y_pred_class = 1

                y_true_dict[entity].append(y_true_class)
                y_pred_dict[entity].append(y_pred_class)
            
            correct_preds.append(ground_truth_dict == prediction_dict)
            
            
        return y_true_dict, y_pred_dict, correct_preds

 
def main():
    # Load data for evaluation
    evaluation_file_name = "./Test_files/v5/evaluation_test-05.json"
    with open(evaluation_file_name, "r") as f:
        ground_truth = json.load(f)

    entities_name = ["From", "To", "Departure_date", "Return_date", "budget"]

    perf_ev = performance_evaluator(ground_truth, entities_name)

    print("\n----------- performances evaluation -------------")
    print("Sample size : ", len(ground_truth))

    # Evaluate intents prediction performance
    precision, recall, fscore = perf_ev.evaluate_intents_performance()
    print("\nIntents performances")
    print("\tPrecision = {:.2f}".format(precision))
    print("\tRecall = {:.2f}".format(recall))
    print("\tF-score = {:.2f}".format(fscore))

    # Evaluate entities prediction performance 
    print("\nEntities performance")
    y_true_dict, y_pred_dict, correct_preds = perf_ev.evaluate_entities_performance()

    for entity in y_true_dict:
        precision, recall, fscore, _ = precision_recall_fscore_support(y_true_dict[entity],
                                                                    y_pred_dict[entity],
                                                                    average="binary")
        print(f"\nentity '{entity}'")
        print("\tprecision = {:.2f}".format(precision))
        print("\trecall = {:.2f}".format(recall))
        print("\tF-score= {:.2f}".format(fscore))

    # Evaluate accuracy
    correct_preds_count = 0
    for i in correct_preds:
        correct_preds_count += correct_preds[i]
    accuracy = correct_preds_count / len(correct_preds)
    print("\nAccuracy = {:.0%}".format(accuracy))

if __name__ == "__main__":
    main()