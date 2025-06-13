import requests
import os


def upload_to_imgbb(image_path):
    key = "3aafe473d7d4bfd3de27262bc3c8013b"
    url = "https://api.imgbb.com/1/upload"

    if not os.path.exists(image_path):
        print(f" File does not exist: {image_path}")
        return None

    try:
        with open(image_path, "rb") as file:
            response = requests.post(url, data={"key": key}, files={"image": file})

        if response.status_code == 200:
            return response.json()["data"]["url"]  # This is the direct display URL
        else:
            print(" Upload failed. Status:", response.status_code)
            print("️ Response text:", response.text)
            return None

    except Exception as e:
        print(f" Exception while uploading to ImgBB: {e}")
        return None


def reverse_image_search(image_path):
    serpapi_key = "20a48469312d362e9a6a7dabaa41393b2b228f797f1467c17b41d720ede65add"
    print(f" Uploading image for reverse search: {image_path}")
    image_url = upload_to_imgbb(image_path)
    if not image_url:
        print(" No image URL returned. Skipping search.")
        return []
    results = []
    try:
        for engine, result_key in [("google_lens", "visual_matches"), ("yandex_images", "image_results")]:
            params = {
                "engine": engine,
                "url": image_url,
                "api_key": serpapi_key
            }
            response = requests.get("https://serpapi.com/search.json", params=params)
            print(f" SerpAPI status code: {response.status_code}")
            data = response.json()

            if data.get("error"):
                print(f" SerpAPI with engine={engine} error: {data['error']}")
                # Only skip if the result_key is also missing
                if not data.get(result_key):
                    continue

            if data.get(result_key):
                # add new items to the list
                results.extend(data.get(result_key))

            print(f" SerpAPI JSON response from {engine}:")
            # print it pretty
            from pprint import pprint
            pprint(data)

        return results

    except Exception as e:
        print(f" Exception during reverse search: {e.with_traceback()}")
        return []
