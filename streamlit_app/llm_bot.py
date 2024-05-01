import requests

def llama_bot(msg, api_url, headers, personality_prompt):
    payload = {
        "inputs": personality_prompt + "\n\nUser: " + msg + "\nAssistant:",
        "max_new_tokens": 1000,  # Increase the maximum number of tokens in the response
    }
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        if isinstance(response_data, list) and len(response_data) > 0:
            generated_text = response_data[0]['generated_text']
            prompt_end_idx = generated_text.find("\nAssistant:")
            if prompt_end_idx != -1:
                actual_response = generated_text[prompt_end_idx + len("\nAssistant:"):].strip()
                return actual_response
            else:
                print("Unexpected response format:", response_data)
                return "Sorry, I couldn't process your request."
        else:
            print("Unexpected response format:", response_data)
            return "Sorry, I couldn't process your request."
    else:
        print(f"API request failed with status code {response.status_code}: {response.text}")
        return "Sorry, there was an error processing your request."
