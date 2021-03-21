import program.evaluate_performance as script
import json
import requests
import pytest


class MockResponse:

    @staticmethod
    def json():
        file_name = "./administration_scripts/predictions.json"
        with open(file_name, "r") as f:
            json_data = json.load(f)
        return json_data[0]


class TestPerformanceEvaluator:
    """
    Set of unit tests to validate the Luis performance evaluation script. This class uses a couple of json files stored
    in the same folder as this code.
    """

    ground_truth_file_name = "./administration_scripts/ground_truth.json"
    with open(ground_truth_file_name, 'r') as f:
        ground_truth = json.load(f)

    entities_name = ["From", "To", "Departure_date", "Return_date", "budget"]
    turn = ground_truth[0]
    text = turn["text"]
    evaluator = script.performance_evaluator(ground_truth, entities_name)


    @pytest.fixture
    def mock_response(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockResponse()
        monkeypatch.setattr(requests, "get", mock_get)


    # get prediction
    def test_get_prediction(self, mock_response):
        
        prediction_file_name = "./administration_scripts/prediction.json"
        with open(prediction_file_name, "r") as f:
            target_prediction = json.load(f)
        prediction = self.evaluator.get_prediction(self.text)
        assert prediction == target_prediction


    # get_ground_truth_entity
    def test_ground_truth_entity(self, mock_response):
        target_from_entity = "Caprica"
        prediction = self.evaluator.get_prediction(self.text)
        entities = prediction["prediction"]["entities"]["$instance"]
        entity_name = "From"
        from_entity = self.evaluator.get_ground_truth_entity(entities, entity_name)
        assert from_entity == target_from_entity


    # evaluate_intents_performance
    def test_evaluate_intents_performance(self, mock_response):
        precision, recall, fscore = self.evaluator.evaluate_intents_performance()
        assert (precision, recall, fscore) == (1, 1, 1)


    # get_ground_truth_entity
    def test_build_dictionnary(self):      
        evaluator = script.performance_evaluator(self.turn, self.entities_name)
        ground_truth_dict, predictions_dict = evaluator.build_dictionnaries(self.turn)
        assert ground_truth_dict == {'From': 'Caprica', 'To': 'Atlantis', 'Departure_date': '', 'Return_date': '', 'budget': '1700'}


