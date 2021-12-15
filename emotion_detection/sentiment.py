from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline


# init class for inference
class SemanticRu:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("static/rubert-base-cased-sentiment-new")
        self.model = AutoModelForSequenceClassification.from_pretrained("static/rubert-base-cased-sentiment-new")
        self.sentiment = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)

    def inference(self, txt):
        """
        :param txt: text for input
        :return: output from predict with label (negative, positive or neutral)
        """
        predict_sentiment = self.sentiment(txt)[0]["label"]
        score = self.sentiment(txt)[0]["score"]

        return predict_sentiment.lower(), score
