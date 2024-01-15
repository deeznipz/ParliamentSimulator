import requests

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def infer_speaker_changes(text, api_key):
    sentences = text.split(". ")
    speakers = []
    identified_speakers = {}
    speaker_count = 0

    for i in range(len(sentences)):
        if i == 0:
            speaker_count += 1
            identified_speakers[speaker_count] = sentences[i]
            speakers.append(f"Speaker {speaker_count}")
            continue

        previous_sentence = sentences[i - 1]
        current_sentence = sentences[i]
        conversation_context = f"{previous_sentence}. {current_sentence}"

        # Crafting a prompt for GPT-4
        prompt = f"Given the conversation: '{conversation_context}', is the current sentence spoken by a new speaker? If yes, does this new speaker sound like any of the previous speakers?"

        # GPT-4 API call (placeholder)
        response = requests.post(
            "https://api.openai.com/v1/engines/gpt-4/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"prompt": prompt, "max_tokens": 50}
        )
        prediction = response.json().get('choices', [{}])[0].get('text', '').strip().lower()

        # Inferring speaker change
        if "new speaker" in prediction:
            speaker_identified = False
            for speaker_id, speaker_text in identified_speakers.items():
                if speaker_text in prediction:
                    speakers.append(f"Speaker {speaker_id}")
                    speaker_identified = True
                    break
            if not speaker_identified:
                speaker_count += 1
                identified_speakers[speaker_count] = current_sentence
                speakers.append(f"Speaker {speaker_count}")
        else:
            speakers.append(speakers[-1])  # Continue with the same speaker

    return speakers

def write_output_file(speaker_labels, sentences, output_file_path):
    with open(output_file_path, 'w') as file:
        for speaker, sentence in zip(speaker_labels, sentences):
            file.write(f"{speaker}: {sentence}\n")

def process_file(file_path, api_key, output_file_path):
    try:
        text = read_text_file(file_path)
        sentences = text.split(". ")
        speaker_labels = infer_speaker_changes(text, api_key)
        write_output_file(speaker_labels, sentences, output_file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Example usage
api_key = "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"
file_path = "C:/Users/deezn/Desktop/py/Transcripts/SeymChloeAM.txt"
output_file_path = "C:/Users/deezn/Desktop/py/Transcripts/SeymChloeAMSpeakers.txt"
process_file(file_path, api_key, output_file_path)
