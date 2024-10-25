import requests
import base64
import time
import io
import base64
from PIL import Image




ERROR_KEY = "GPT4VError"  # The presence of this string in the results can be used as an indicator of whether an error has occurred


def request(
    img,
    prompt_sys,
    prompt_user,
    timeout=30,
    max_tokens=512,
    apikey=0,
    compress_rate=95,
):
    try:
        # img = Image.open(imgpath)

        """ The use of abbreviations can result in significant differences in output structures, so they are not currently being employed. 
        width, height = img.size                
        if width > 1024 or height > 1024:
            max_size = (1024,1024)
            img.thumbnail(max_size, Image.ANTIALIAS)   
        """

        buffered = io.BytesIO()
        # img.save("/home/starmage/projects/uicoder/output/F5FFC91C-2C64-4DB8-9008-F040CF1F2146.png", format=img.format, quality=compress_rate)
        img.save(
            buffered, format=img.format, quality=compress_rate
        )  
        encoded_image = base64.b64encode(buffered.getvalue()).decode("ascii")
    except Exception as e:
        return f"Failed to make the request. {ERROR_KEY}: {e}"
    headers = {
        "Content-Type": "application/json",
        "api-key": 'gpt-v4_key_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    }

    # Payload for the request
    payload = {
        "messages": [
            {"role": "system", "content": [{"type": "text", "text": prompt_sys}]},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                    {
                        "type": "text",
                        "text": prompt_user,
                    },
                ],
            },
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": max_tokens,
    }

    # GPT4V_ENDPOINT = "https://gpt4v-test-rp.openai.azure.com/openai/deployments/IMG-TXT/chat/completions?api-version=2023-07-01-preview"
    GPT4V_ENDPOINT = f"gpt-4v-url-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    # Send request
    try:
        response = requests.post(
            GPT4V_ENDPOINT, headers=headers, json=payload, timeout=timeout
        )
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        # Handle the response as needed (e.g., print or process)
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return content
    except requests.RequestException as e:
        return f"Failed to make the request. {ERROR_KEY}: {e}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image_path", type=str, required=True)
    parser.add_argument(
        "-p1",
        "--prompt_system",
        type=str,
        default="You are an ai assitant to help people find information.",
    )
    parser.add_argument(
        "-p2",
        "--prompt_user",
        type=str,
        default="Give some description about the input image.",
    )
    parser.add_argument("-t", "--timeout", type=int, default=30)
    parser.add_argument("-c", "--compress_rate", type=int, default=95)
    parser.add_argument("-m", "--max_tokens", type=int, default=512)
    parser.add_argument("-k", "--gpt4v_key", type=int, default=0, choices=[0, 1, 2, 3])

    args = parser.parse_args()

    content = request(
        args.image_path,
        args.prompt_system,
        args.prompt_user,
        args.timeout,
        args.max_tokens,
        args.gpt4v_key,
        args.compress_rate,
    )
    print(content)
