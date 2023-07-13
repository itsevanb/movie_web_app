import json
from .data_manager_interface import DataManagerInterface
from werkzeug.security import generate_password_hash

class JSONDataManager(DataManagerInterface):
    #Initialize the class with the file name
    def __init__(self, file_name):
        self.file_name = 'movie_web_app/datamanager/' + file_name

    def _read_data(self):
        #Open the file and read the data
        try:
            with open(self.file_name, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"An error occurred while reading the data: {str(e)}")
            return []
        
    def _write_data(self, data):
        #Open the file and write the data
        try:
            with open(self.file_name, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"An error occurred while writing the data: {str(e)}")

    def get_all_users(self):
        #Return all users
        return self._read_data()
    
    def get_user_movies(self, user_id):
        #Return all movies for a user
        users = self.get_all_users()
        for user in users:
            if user['id'] == user_id:
                return user.get('movies', [])
        print(f"User with id {user_id} not found.")
        return []
    
    def add_user(self, name, username, password):
        #Add a new user
        try:
            users = self._read_data()
            new_user_id = max([user['id'] for user in users], default = 0) + 1
            hashed_password = generate_password_hash(password)
            new_user = {
                'id': new_user_id,
                'name': name,
                'username': username,
                'password': hashed_password,
                'movies': []
            }
            users.append(new_user)
            self._write_data(users)
        except Exception as e:
            print(f"An error occurred while adding the user: {str(e)}")

    def remove_user(self, user_id):
        #Remove a user
        users = self.get_all_users()
        users = [user for user in users if user['id'] != user_id]
        self._write_data(users)

    def add_movie(self, user_id, movie):
        #Add a movie for a user
        users = self.get_all_users()
        for user in users:
            if user['id'] == user_id:
                user['movies'].append(movie)
        self._write_data(users)

    def update_movie(self, user_id, movie_id, updated_movie):
        #Update a movie for a user
        data = self._read_data()
        for user in data:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        movie.update(updated_movie)
                        break
        self._write_data(data)

    def delete_movie(self, user_id, movie_id):
        #Remove a movie for a user
        users = users = self.get_all_users()
        for user in users:
            if user['id'] == user_id:
                user['movies'] = [movie for movie in user['movies'] if int(movie['id']) != int(movie_id)]
        self._write_data(users)