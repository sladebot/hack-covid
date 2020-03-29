from api import GiphyAPI

def main():
    api = GiphyAPI()
    api.searchGif("trump")

if __name__ == "__main__":
    main()