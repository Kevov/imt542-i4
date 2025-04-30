import openai
import base64
import requests
import json


CURR_DIR = 'C:\\Users\\khoal\\Desktop\\imt542\\imt542-i4\\'

# Load API key from a file
def load_api_key(filename='openai_api_key.txt'):
    fullPath = CURR_DIR + filename
    with open(fullPath, 'r') as file:
        return file.read().strip()

def crawl_raw_html(url):
    fullPath = CURR_DIR + 'output.html'
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(fullPath, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print("HTML saved to output.html")
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}")
    
    return response.text

def steam_game_json():
    url = 'https://store.steampowered.com/api/appdetails?appids=10'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Get Games Detail Failed failed: {response.status_code} - {response.text}")

def save_to_json(data, filename):
    fullDir = CURR_DIR + filename
    with open(fullDir, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_img(filename):
    fullDir = CURR_DIR + filename

    client = openai.OpenAI(api_key = load_api_key())

    with open(fullDir, 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Send to GPT-4 with vision
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    # Print the description
    return response.choices[0].message.content

if __name__ == "__main__":
    openai.api_key = load_api_key()

    try:
        print("\nFetching Steam Game Summary...")
        game_data = steam_game_json()
        save_to_json(game_data, 'game_summary.json')
        print("Game summary saved to game_summary.json")
        print("Getting image data from example.png and sending it to chatGPT for description")
        desc = load_img('example.jpg')
        print("ChatGPT description:" + desc)
        print("Crawling an HTML page")
        raw_html = crawl_raw_html('https://kevov.github.io/my-hero-website/')
        print("Raw HTML:")
        print(raw_html)

    except Exception as e:
        print(f"Error: {e}")
