import boto3
import logging
from botocore.exceptions import ClientError

class Analyser:
	def __init__():
		try:
			client = boto3.client('comprehend')

	def get_sentiment_analysis(feed):
		if feed == "":
			print("Input feed is empty")
			return
		try:
			response = client.detect_sentiment(Text=feed, LanguageCode='en')			
		except botocore.exceptions.ClientError as e:
			logging.exception("Not able to authenticate " + e)

		return response