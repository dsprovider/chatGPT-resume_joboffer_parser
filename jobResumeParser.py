import os
import csv
import fitz
import json
import pprint
from datetime import datetime

import openai
from openai import OpenAI


OPENAI_API_KEY="sk-proj-IUFCBJlSK8LJfJ7uQjoZT3BlbkFJeUVnpTEHorsVspt1GLee"
openai.api_key=OPENAI_API_KEY
print(openai.api_key)

# ===================================================================================================

def read_pdf(file_path):
    pdf_document = fitz.open(file_path)
    text = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    
    pdf_document.close()
    
    return text

# ===================================================================================================

def process_folder(in_folder, client):
    # model_name = "gpt-3.5-turbo"
    model_name = "gpt-4o"

    i = 0
    for root, dirs, files in os.walk(in_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                data = []
                print(f">> [{i}] *** {file} *** ")
                file_path = os.path.join(root, file)

                try:
                    text = read_pdf(file_path)
                    
                    # --- [A] --- resume prompt ---
                    # prompt = f"""
                    # Parse the following resume '{text}' into these exact sections: 'contact_details', 'summary', 'hard_skills', 
                    # 'soft_skills', 'working_experience', 'education', 'languages', 'certificates' and 'projects'. 
                    # For 'languages' (spoken languages, not programming languages), provide a list of strings.
                    # Output the response in JSON format with each section name as a key and the 
                    # parsed content as the value. Do not include `json at the beginning or ` at the end of the response. 
                    # Do not include line breaks in the key names. For 'contact_details', include 
                    # these exact subsections 'fullname', 'address', 'email', 'phone_number', 'linkedin_profile', 'github_repository' and any 
                    # other personal detail information that applies. For 'working_experience', 'projects' and 'education' sections, 
                    # parse them into a list of objects, each object containing 'time_period' and 'description' as keys, 
                    # where 'description' is a single string. For 'summary', provide a single string. 
                    # For 'soft_skills', 'hard_skills', 'certificates' and 'languages' provide a list of strings. 
                    # Only include subsections for 'contact_details' as previously detailed. Also, include a 'lang' key at the 
                    # beginning of the JSON object to indicate the language of the parsed text. 
                    # Indicate the full name of the language of the parsed text; do not use abbreviations. 
                    # Finally, do not translate the text; parse it as is. Keep the original language.
                    # """
                    # template_prompt = "Parse the following resume '<text>' into these exact sections: 'contact_details', 'summary', 'hard_skills',  'soft_skills', 'working_experience', 'education', 'languages', 'certificates' and 'projects'.  For 'languages' (spoken languages, not programming languages), provide a list of strings. Output the response in JSON format with each section name as a key and the  parsed content as the value. Do not include line breaks in the key names. For 'contact_details', include  these exact subsections 'fullname', 'address', 'email', 'phone_number', 'linkedin_profile', 'github_repository' and any  other personal detail information that applies. For 'working_experience', 'projects' and 'education' sections,  parse them into a list of objects, each object containing 'time_period' and 'description' as keys,  where 'description' is a single string. For 'summary', provide a single string.  For 'soft_skills', 'hard_skills', 'certificates' and 'languages' provide a list of strings.  Only include subsections for 'contact_details' as previously detailed. Also, include a 'lang' key at the  beginning of the JSON object to indicate the language of the parsed text.  Indicate the full name of the language of the parsed text; do not use abbreviations.  Finally, do not translate the text; parse it as is. Keep the original language."

                    
                    # --- [B] --- job offer prompt ---
                    prompt = f"""
                    Parse the following job offer '{text}' into these exact sections: 'company', 'job_description', 
                    'required_hard_skills', 'required_soft_skills', 'experience_years_required', 'required_studies', 'required_languages'
                    and 'benefits'. For 'company', 'experience_years_required' and 'job_description' provide a string. 
                    For 'required_hard_skills', 'required_soft_skills', 'required_studies', 
                    'required_languages' (spoken languages, not programming languages) and 'benefits' provide a list of strings.
                    Output the response in JSON format with each section name as a key
                    and the parsed content as the value. 
                    Do not include `json at the beginning or ` at the end of the response. Do not include line breaks in the key names. Also, include 
                    a 'lang' key at the beginning of the JSON object to indicate the language of the parsed text.
                    Indicate the full name of the language of the parsed text; do not use abbreviations.
                    Finally, do not translate the text. Parse it as is, keeping the original language.
                    """
                    template_prompt = "Parse the following job offer '<text>' into these exact sections: 'company', 'job_description',  'required_hard_skills', 'required_soft_skills', 'experience_years_required', 'required_studies', 'required_languages' and 'benefits'.For 'company', 'experience_years_required' and 'job_description' provide a string.  For 'required_hard_skills', 'required_soft_skills', 'required_studies',  'required_languages' (spoken languages, not programming languages) and 'benefits' provide a list of strings. Output the response in JSON format with each section name as a key and the parsed content as the value. Do not include line breaks in the key names. Also, include  a 'lang' key at the beginning of the JSON object to indicate the language of the parsed text. Indicate the full name of the language of the parsed text; do not use abbreviations. Finally, do not translate the text. Parse it as is, keeping the original language."

                    response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )

                    response_content = response.choices[0].message.content
                    json_response = json.loads(response_content)
                    pprint.pprint(json_response)

                    usage = response.usage
                    completion_tokens = usage.completion_tokens
                    prompt_tokens = usage.prompt_tokens
                    total_tokens = usage.total_tokens

                    print(f"[+] completion_tokens: {completion_tokens}")
                    print(f"[+] prompt_tokens: {prompt_tokens}")
                    print(f"[+] total_tokens: {total_tokens}")

                    # Write to CSV logger (API execution logger)
                    header = ["timestamp", "gptmodel", "file", "input_prompt", "completion_tokens", "prompt_tokens", "total_tokens"]
                    csv_logfile = os.path.join(os.getcwd(), "master_api_logger.csv")
                    
                    current_timestamp = str(datetime.now())
                    data = [current_timestamp, model_name, str(file), template_prompt, completion_tokens, prompt_tokens, total_tokens]

                    file_exists = os.path.isfile(csv_logfile)
                    with open(csv_logfile, mode='a', newline='', encoding="utf-8") as csv_file:
                        writer = csv.writer(csv_file, delimiter='|')
                        if not file_exists:
                            writer.writerow(header)
                        
                        writer.writerow(data)                     
                    
                    # Write to JSON object
                    out_file = os.path.join(in_folder, file.replace(".pdf", "") + f"_{model_name}.json")
                    with open(out_file, "w", encoding="utf-8") as json_file:
                        json.dump(json_response, json_file, ensure_ascii=False, indent=4)

                    print("--------------------------------------------------------------------")
                except Exception as e:
                    print(f">> Error message: {str(e)}. {type(e)}")
                i += 1

# ===================================================================================================

def main():

    # Resumes folder
    # in_resumes_dir = os.path.join(os.getcwd(), "resumes")

    # Offers foler
    in_offers_dir = os.path.join(os.getcwd(), "offers")

    client = OpenAI(api_key=OPENAI_API_KEY)
    print(">> [DONE] ... OpenAI client created!")

    process_folder(in_offers_dir, client)

if __name__ == '__main__':
    main()