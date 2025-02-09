import requests
import pandas as pd
import re
from tqdm import tqdm

# the LM Studio API endpoint
API_URL = ""  

# Load dataset
df = pd.read_csv("ielts_writing_dataset.csv") 

def get_range_accuracy_score(essay_text):
    prompt = f"""
    You are an expert IELTS examiner. Assess the following essay based on the IELTS Grammatical Range & Accuracy band descriptors.

    Use the following official IELTS band descriptors to assign a score:

    Score 8.5-9:
    A wide range of structures is used with full flexibility and control.
    Punctuation and grammar are used appropriately throughout.
    Minor errors are extremely rare and have minimal impact on communication.

    Score 7.5-8.0:
    A wide range of structures is flexibly and accurately used.
    The majority of sentences are error-free, and punctuation is well managed.
    Occasional, non-systematic errors and inappropriacies occur, but have minimal impact on communication.

    Score 6.5-7.0:
    A variety of complex structures is used with some flexibility and accuracy.
    Grammar and punctuation are generally well controlled, and error-free sentences are frequent.
    A few errors in grammar may persist, but these do not impede communication.

    Score 5.5-6.0:
    A mix of simple and complex sentence forms is used but flexibility is limited.
    Examples of more complex structures are not marked by the same level of accuracy as in simple structures.
    Errors in grammar and punctuation occur, but rarely impede communication.

    Score 4.5-5.0:
    The range of structures is limited and rather repetitive.
    Although complex sentences are attempted, they tend to be faulty, and the greatest accuracy is achieved on simple sentences.
    Grammatical errors may be frequent and cause some difficulty for the reader.
    Punctuation may be faulty.

    Score 3.5-4.0:
    A very limited range of structures is used.
    Subordinate clauses are rare and simple sentences predominate.
    Some structures are produced accurately but grammatical errors are frequent and may impede meaning.
    Punctuation is often faulty or inadequate.

    Score 2.5-3.0:
    Sentence forms are attempted, but errors in grammar and punctuation predominate (except in memorised phrases or those taken from the input material). This prevents most meaning from coming through.
    Length may be insufficient to provide evidence of control of sentence forms.

    Score 1.5-2.0:
    There is little or no evidence of sentence forms (except in memorised phrases).

    Score 1.0:
    Responses of 20 words or fewer are rated at Band 1.
    No resource is apparent, except for a few isolated words.

    Essay for Evaluation
    {essay_text}

    Task: Assign a single IELTS band score from 1.0 to 9.0, based only on grammatical range & accuracy. Return only the score, no explanations.
    """

    payload = {
        "model": "",  
        "prompt": prompt,
        "max_tokens": 10,
        "temperature": 0.2,
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        return extract_number(result["choices"][0]["text"])  
    else:
        return None  


def extract_number(text):
    match = re.search(r'\d+(\.\d+)?', text)  # gotta make sure to get the decimal number when needed.
    return float(match.group()) if match else None


tqdm.pandas()  # good progress bar
df["Range_Accuracy"] = df["Essay"].astype(str).progress_apply(get_range_accuracy_score)

df.to_csv("updated_ielts_writing_dataset.csv", index=False)

print("Grammatical Range & Accuracy scores have been successfully added!")
