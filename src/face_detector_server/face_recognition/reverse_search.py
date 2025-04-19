import requests
import os

def upload_to_imgbb(image_path):
    key = "360a3efb7dfbde0e52e54c14f457f672"
    url = "https://api.imgbb.com/1/upload"

    if not os.path.exists(image_path):
        print(f"❌ File does not exist: {image_path}")
        return None

    try:
        with open(image_path, "rb") as file:
            response = requests.post(url, data={"key": key}, files={"image": file})

        if response.status_code == 200:
            return response.json()["data"]["url"]  # This is the direct display URL
        else:
            print("⚠️ Upload failed. Status:", response.status_code)
            print("⚠️ Response text:", response.text)
            return None

    except Exception as e:
        print(f"❌ Exception while uploading to ImgBB: {e}")
        return None


def reverse_image_search(image_path):
    serpapi_key = "037aa4ce80f1e408c081476a8669b0b2aaac654acdedadc36657392675199700"

    print(f"🔍 Uploading image for reverse search: {image_path}")
    image_url = upload_to_imgbb(image_path)
    if not image_url:
        print("❌ No image URL returned. Skipping search.")
        return []

    try:
        params = {
            "engine": "google_lens",
            "url": image_url,
            "api_key": serpapi_key
        }
        response = requests.get("https://serpapi.com/search.json", params=params)

        print(f"📦 SerpAPI status code: {response.status_code}")
        data = response.json()
        print("📑 SerpAPI JSON response:")
        from pprint import pprint
        pprint(data)

        if "error" in data:
            print(f"❌ SerpAPI error: {data['error']}")
            return []

        return data.get("visual_matches", [])

    except Exception as e:
        print(f"❌ Exception during reverse search: {e}")
        return []
