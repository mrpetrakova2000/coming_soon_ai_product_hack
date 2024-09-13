import openai
import pandas as pd

def get_last_50_percent_of_dataframe(df):
    """Returns the last 50% of rows from a DataFrame"""
    total_rows = len(df)
    start_index = total_rows // 2  # Start from the halfway point
    last_half_df = df.iloc[start_index:].reset_index(drop=True)
    return last_half_df

def read_prompt_from_txt(prompt_file_path):
    """Reads a prompt from a text file and returns it"""
    with open(prompt_file_path, 'r') as file:
        prompt = file.read()
    return prompt

def prepare_final_prompt(prompt, df):
    """Combines the prompt from the text file and the DataFrame data"""
    final_prompt = prompt + "\n\nHere is the data:\n"
    final_prompt += df.to_csv(index=False)
    return final_prompt

def send_dataframe_to_chatgpt(input_df):
    """Sends the DataFrame content along with a custom prompt to OpenAI GPT and gets the response"""
    # Get the last 50% of the DataFrame
    df = input_df[['cnt', 'item_id', 'date']] 
    last_half_df = get_last_50_percent_of_dataframe(df)

    # Read the custom prompt from the text file
    prompt_file_path = 'backend/ml_pipeline/assets/prompt.txt'   #TODO: make it not hard-coded
    prompt = read_prompt_from_txt(prompt_file_path)

    # Prepare the final prompt
    final_prompt = prepare_final_prompt(prompt, last_half_df)

    # Prepare the messages for the chat model
    messages = [
        {"role": "system", "content": "You are a data analyst assistant and you make a business decisions."},
        {"role": "user", "content": final_prompt}
    ]

    # Make the API call to OpenAI using ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-4o",  
        messages=messages,
        max_tokens=700  # Adjust as needed
    )

    return response['choices'][0]['message']['content']




# HOW TO USE
# csv_file_path = 'item_064.csv'         # Path to your CSV file
# data = pd.read_csv(csv_file_path)
# response_text = send_dataframe_to_chatgpt(data, prompt_file_path)
# print(response_text)