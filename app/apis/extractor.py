from app.models.model import model
from fastapi import APIRouter, Form
import re
from pydantic import BaseModel

router = APIRouter()


prompt = """
You are an information extraction assistant.

Your task is to extract a list of "Information Units" from the given novel passage. You need to Extract Information Units covering all key actions in the passage. 
Here is the style. 
'Subject (who), Event (what), Time (when), Location (where)'
Example output format:
Kevin,Accepted a call from Lucy to assist in theft,One day,N/A  

Use a structured output format: Each Information Unit should be on a new line, with fields separated by commas ,.
If time or location is not mentioned, write "N/A".
The order of fields must be: Subject, Event, Time, Location.
DON'T reply with any additional text or explanation. Just provide the extracted Information Units in the specified format.

The novel passage:

'{}'

"""


# prompt = """
# Summarize and Extract a list of 'No., Subject/who, Event/what, Time/when, Location/where' from the given novel passage, with No Preamble, No Explanation.

# Your example output format should be:
# (No., Subject/who, Event/what, Time/when, Location/where) 
# 1, Kevin, Accepted a call from Lucy to assist in theft, One day, N/A  
# 2, ...
# 3, ...

# The novel passage:

# '{}'

# """

# class ExtractRequest(BaseModel):
#     novel_passage: str

@router.post("/extract_info")
def extract_information_units(novel_passage: str = Form(...)):

    full_prompt = prompt.format(novel_passage)
    print("Full_prompt:", full_prompt)
    result = extract_info(full_prompt)

    extracted_units = parse_extracted_info(result)
    # # Split the result into lines and filter out empty lines
    # lines = [line.strip() for line in result.split("\n") if line.strip()]

    # # Use regex to extract the fields from each line
    # extracted_units = []
    # for line in lines:
    #     match = re.match(r'([^,]+),([^,]+),([^,]+),([^,]+)', line)
    #     if match:
    #         subject, event, time, location = match.groups()
    #         extracted_units.append({
    #             "Subject": subject.strip(),
    #             "Event": event.strip(),
    #             "Time": time.strip(),
    #             "Location": location.strip()
    #         })

    return {"extracted_units": extracted_units}

def extract_info(text):
    result = model.generate(text, role="You are an information extraction assistant.", max_new_tokens=2048, temperature=0.9, top_k=50, top_p=0.95)
    print("Full response:", result)
    return result

def parse_extracted_info(text):
    """
    Parse the extracted information units into a structured list of dicts.
    Each line is expected to have 4 fields separated by commas: who, what, when, where.
    """
    parsed_units = []
    lines = text.strip().split('\n')
    print(lines)
    
    for line in lines:
        fields = [field.strip() for field in line.split(',')]
        if len(fields) != 4:
            print(f"Warning: Line does not have 4 fields -> {line}")
            continue
        unit = {
            "who": fields[0],
            "what": ''.join(fields[1:-2]),
            "when": fields[-2],
            "where": fields[-1]
        }
        parsed_units.append(unit)
    
    return parsed_units
