import boto3
import logging
from botocore.exceptions import ClientError
from app.giphy import GiphyAPI

class SentimentAnalyser:
	client = None
	giphy_client = None
	def __init__(self):
		try:
			self.giphy_client = GiphyAPI()
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

	def get_sentiment_scores(self, feeds):
		result = {
			"NEGATIVE" : [],
			"POSITIVE" : [],
			"NEUTRAL" : []
		}
		for article in feeds:
			title = article.get("title")
			description = article.get("description")
			input_feed = title + " " + description
			words = input_feed.split()

			separator = ' '
			if len(words) > 250:
				input_feed = separator.join(words[:250])

			analysis = self.get_sentiment_analysis(input_feed)

			if analysis is not None:
				sentiment_result = {
					"Sentiment" : analysis.get("Sentiment"),
					"Score" : analysis.get("SentimentScore"),
					"Giphy" : None
				}

				#TODO: Revist this logic to determine the threshold for negative news
				if sentiment_result.get("Sentiment") == "NEGATIVE":
				    sentiment_result["Giphy"] = self.giphy_client.searchHappyGif()
				elif sentiment_result.get("Sentiment") == "NEUTRAL":
					sentiment = sentiment_result.get("SentimentScore")
					if sentiment["Negative"] >= 0.01 and sentiment["Negative"] > sentiment["Positive"]:
						sentiment_result["Giphy"] = self.giphy_client.searchHappyGif()

				if sentiment_result["Giphy"] is not None:
					result["NEGATIVE"].append(sentiment_result)
				elif sentiment_result["Sentiment"] == "POSITIVE":
					result["POSITIVE"].append(sentiment_result)
				else:
					result["NEUTRAL"].append(sentiment_result)

		
		return result