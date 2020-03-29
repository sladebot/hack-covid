import boto3
import logging
from botocore.exceptions import ClientError

class SentimentAnalyser:
	client = None
	def __init__(self):
		try:
			self.client = boto3.client('comprehend')
		except botocore.exceptions.ClientError as e:
			logging.exception("Not able to authenticate " + str(e))

	def get_sentiment_analysis(self, feed):
		if feed == "":
			loggin.error("Input feed is empty")
			return
		try:
			if self.client is not None:
				response = self.client.detect_sentiment(Text=feed, LanguageCode='en')
			else:
				logging.exception("Client not initialized")
		except botocore.exceptions.ClientError as e:
			logging.exception("Not able to process the request : " + str(e))

		return response