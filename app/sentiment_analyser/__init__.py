import boto3
import logging
import botocore
from botocore.exceptions import ClientError
from app.giphy import GiphyAPI
import hashlib

class SentimentAnalyser:
	client = None
	giphy_client = None
	cache = {}
	def __init__(self):
		try:
			self.giphy_client = GiphyAPI()
			self.client = boto3.client('comprehend')
		except botocore.exceptions.ClientError as e:
			logging.exception("Not able to authenticate " + str(e))

	def get_sentiment_analysis(self, feed):
		if feed == "":
			logging.error("Input feed is empty")
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

			input_hash = hashlib.md5(input_feed.encode('utf-8')).hexdigest()
			if input_hash not in self.cache:
				analysis = self.get_sentiment_analysis(input_feed)
				self.cache[input_hash] = analysis
			else:
				analysis = self.cache[input_hash]

			if analysis is not None:
				sentiment_result = {
					"Sentiment": analysis.get("Sentiment"),
					"Score": analysis.get("SentimentScore"),
					"Giphy": None,
					"title": title,
					"description": description,
					"link": article.get("link")
				}

				# TODO: Revist this logic to determine the threshold for negative news
				if sentiment_result.get("Sentiment") == "NEGATIVE":
					sentiment_result["Giphy"] = self.giphy_client.searchHappyGif()
				elif sentiment_result.get("Sentiment") == "NEUTRAL":
					sentiment = sentiment_result.get("SentimentScore")
					if sentiment is not None and (
							sentiment["Negative"] >= 0.01 and sentiment["Negative"] > sentiment["Positive"]):
						sentiment_result["Sentiment"] = "NEGATIVE"
						sentiment_result["Giphy"] = self.giphy_client.searchHappyGif()

				if sentiment_result["Giphy"] is not None:
					result["NEGATIVE"].append(sentiment_result)
				elif sentiment_result["Sentiment"] == "POSITIVE":
					result["POSITIVE"].append(sentiment_result)
				else:
					result["NEUTRAL"].append(sentiment_result)

		mixed_feeds = self.balance_feeds(result)

		return mixed_feeds

	def get_giphy_mock(self):
		return "www.mockgiphy.com"

	def balance_feeds(self, feeds):
		negative_feeds = len(feeds["NEGATIVE"])
		positive_feeds = len(feeds["POSITIVE"])
		neutral_feeds = len(feeds["NEUTRAL"])

		mixed_feeds = []
		index1 = 0
		index2 = 0
		while index1 < negative_feeds and index2 < positive_feeds:
			mixed_feeds.append(feeds["NEGATIVE"][index1])
			index1 = index1 + 1
			mixed_feeds.append(feeds["POSITIVE"][index2])
			index2 = index2 + 1

		while index1 < negative_feeds:
			mixed_feeds.append(feeds["NEGATIVE"][index1])
			index1 = index1 + 1

		while index2 < positive_feeds:
			mixed_feeds.append(feeds["POSITIVE"][index2])
			index2 = index2 + 1

		i=2
		index = 0
		while i < len(mixed_feeds) and index < neutral_feeds:
			mixed_feeds.insert(i, feeds["NEUTRAL"][index])
			i = i+3
			index = index + 1

		if index < neutral_feeds:
			mixed_feeds.append(feeds["NEUTRAL"][index])

		return mixed_feeds





