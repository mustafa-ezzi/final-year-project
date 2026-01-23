import requests

# 1. This is a dummy data URL available in web 
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)

# 2. Now i am displaying the data to terminal 
print("Status Code:", response.status_code)

# 3. now 
data = response.json()
print("Title:", data["title"])
print("Body:", data["body"])
