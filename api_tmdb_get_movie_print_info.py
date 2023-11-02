import os
import requests
import json

class MovieInfoFetcher:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def fetch_movie_info(self):
        # Define the query parameters
        params = {'api_key': self.api_key}

        # Send the GET request
        response = requests.get(self.base_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            movie_data = response.json()
            return movie_data
        else:
            # Print an error message if the request failed
            print(f"Error: {response.status_code}")
            return None

    def print_movie_info(self):
        # Fetch movie information
        movie_data = self.fetch_movie_info()

        if movie_data:
            # Extract and print "homepage" and "overview" fields
            homepage = movie_data.get('homepage')
            overview = movie_data.get('overview')

            if homepage:
                print(f"Homepage: {homepage}")
            else:
                print("Homepage not available")

            if overview:
                print(f"Overview: {overview}")
            else:
                print("Overview not available")

def main():
    # Retrieve the API key from the environment variable
    api_key = os.environ.get('MOVIEDB_API_KEY')

    if api_key is None:
        print("API key not found in environment variable MOVIEDB_API_KEY")
    else:
        # Set the base URL, in this example for Star Wars
        base_url = 'https://api.themoviedb.org/3/movie/11'

        # Create an instance of MovieInfoFetcher with the base URL
        movie_fetcher = MovieInfoFetcher(api_key, base_url)

        # Print movie information
        movie_fetcher.print_movie_info()

if __name__ == "__main__":
    main()
