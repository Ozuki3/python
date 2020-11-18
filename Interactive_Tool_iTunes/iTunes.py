import json
import requests
import webbrowser

# Part 1 & 2
class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json = None):
        if json == None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
        else:
            if "trackName" in json.keys():
                self.title = json["trackName"]
            else:
                self.title = json["collectionName"]
            self.author = json["artistName"]
            self.url = json["collectionViewUrl"]
            self.release_year = json["releaseDate"][0:4]

    def info(self):

        return "{} by {} ({})".format(self.title, self.author, self.release_year)

    def length(self):

        return 0

class Song(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL",\
                 album="No Album", genre="No Genre", track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json == None:
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.url = json["trackViewUrl"]
            self.title = json["trackName"]
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.track_length = int(json["trackTimeMillis"])

    def info(self):

        return "{} by {} ({}) [{}]".format(self.title, self.author, self.release_year, self.genre)

    def length(self):

        return round(self.track_length / 1000)

class Movie(Media):

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating="No Rating", movie_length=0, json = None):
        super().__init__(title, author, release_year, url, json)
        if json == None:
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.url = json["trackViewUrl"]
            self.title = json["trackName"]
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = int(json["trackTimeMillis"])

    def info(self):

        return "{} by {} ({}) [{}]".format(self.title, self.author, self.release_year, self.rating)

    def length(self):

        return round(self.movie_length / 60000)

# Other classes, functions, etc. should go here

#part 3 & 4
if __name__ == "__main__":

    search = input("What would you like to search? Enter a keyword to search or 'exit' to quit:")
    while True:
        if search.lower() == 'exit':
            break

        elif search.isnumeric() is False:
            itunes = "https://itunes.apple.com/search?term="
            response = requests.get(itunes + search.replace(" ", "+")).json() ##一定要有json,这样得到的才是dic

            songs = []
            movies = []
            others = []
            for i in response["results"]:
                if "kind" not in i.keys():
                    others.append(Media(json=i))
                elif i["kind"] == "song":
                    songs.append(Song(json=i))
                elif i["kind"] == "feature-movie":
                    movies.append(Movie(json=i))
                else:
                    others.append(Media(json=i))

            if len(songs) != 0:
                print("\nSONGS\n")
                for i in range(len(songs)):
                    print("{} {}".format(i + 1, songs[i].info()))
            else:
                print("\nSONGS\nNo songs found.\n")
            if len(movies) != 0:
                print("\nMOVIES\n")
                for i in range(len(movies)):
                    print("{} {}".format(len(songs) + 1 + i, movies[i].info()))
            else:
                print("\nMOVIES\nNo movies found.\n")
            if len(others) != 0:
                print("\nOTHER MEDIA\n")
                for i in range(len(others)):
                    print("{} {}".format(len(songs) + len(movies) + 1 + i, others[i].info()))
            else:
                print('OTHER MEDIA\nNo other media found.\n')

        elif search.isnumeric():
            search_list = []
            search_list = songs + movies + others
            if len(search_list) >= int(search):
                web_url = search_list[int(search) - 1].url
                print("Launching {} in web browser...\n".format(web_url))
                webbrowser.open_new_tab(web_url)
            else:
                print("Invalid input: please try another number no more than {}. \n".format(len(search_list)))

        else:
            break

        search = input("Enter the index number to view detail, or another keyword for a new search, or 'exit' to quit: ")

    print('Bye!')
