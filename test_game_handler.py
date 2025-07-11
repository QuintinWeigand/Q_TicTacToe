import requests
def main():
    try:
        response = requests.get('http://127.0.0.1:5000/game_state')
        if response.status_code == 200:
            game_state = response.json()
            print(game_state)  # Print the JSON response as a dictionary
        else:
            print(f"Failed to fetch game state. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__": main()
