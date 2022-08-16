import requests

api_key = "AIzaSyD-HPqZ6715o4r5STSx5mGtlx8vqjTLZNc"
address = "nguyen+van+cu+VN"


def get_current_location():
    ploads = {'things':2,'total':25}
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, api_key)
    response = requests.get(url, ploads).json()

    return response


print(get())