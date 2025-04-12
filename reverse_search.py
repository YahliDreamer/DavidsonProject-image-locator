import requests

def upload_to_imgbb(image_path):
    key = r"360a3efb7dfbde0e52e54c14f457f672"
    url = "https://api.imgbb.com/1/upload"

    with open(image_path, "rb") as file:
        response = requests.post(url, data={"key": key}, files={"image": file})

    if response.status_code == 200:
        return response.json()["data"]["url"]
    else:
        print("Error uploading image:", response.json())
        return None

def reverse_image_search(image_path):
    key = r"037aa4ce80f1e408c081476a8669b0b2aaac654acdedadc36657392675199700"
    image_url = upload_to_imgbb(image_path)
    if not image_url:
        return []

    params = {"engine": "google_lens", "url": image_url, "api_key": key}
    response = requests.get("https://serpapi.com/search.json", params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}")
        return []

    return response.json().get("visual_matches", [])
