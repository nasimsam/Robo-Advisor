import streamlit as st
import openai
from io import BytesIO
from PIL import Image

st.title("Robo Advisor")
user_input= ['' for i in range(8)]
user_input[0] = st.text_input("Please enter your name:")
user_input[1] = st.text_input("Please enter your age:")
user_input[2] = st.text_input("Please enter your annaul income:")
user_input[3] = st.text_input("Please enter your monthly rent/morgage amount:")
user_input[4] = st.selectbox("Please enter your investment horizon:", ["Short term", "Medium term", "Long term"])
user_input[5] = st.text_input("Please enter your investment amount:")
user_input[6] = st.text_input("Please enter your location:")
user_input[7] = st.text_input("Please enter your investment goal:")

api = st.secrets["openai"]
client = openai.OpenAI(api_key= api)
assistant = client.beta.assistants.create(
  name="data analyst assistant",
  instructions="You are a data analyst assistant. Show charts and graphs to help the user understand the data.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4o-mini",
)
thread = client.beta.threads.create()
def Advise(input):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
           
            {"role": "user", "content": f"Please provide a {input[4]} fincial advice for {input[0]} who is {input[1]} years old: given following information: the annaul income is {input[2]}, the monthly rent/morgage is {input[3]}, {input[0]} is living in {input[6]} and {input[0]} has the following investment goals: planning to invest {input[5]} annaully and {input[7]}, also draw a \" Vertical Barchart \" for suggested monthly budget for {input[0]} including Housing (Rent/Mortgage & Utilities), Transportation, Groceries, Dining Out, Health & Insurance, Entertainment & Leisure, Savings & Investments, Miscellaneous."}
        ]
        
    )
    
    advise = response.choices[0].message.content
    return advise
    
def Suggest_Monthly_Budget(input):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
           
            {"role": "user", "content": f"Please suggest monthly budget for {input[0]} in JSON format who is {input[1]} years old containing following keys: 'Housing (Rent/Mortgage & Utilities)', 'Transportation', 'Groceries', 'Dining Out', 'Health & Insurance', 'Entertainment & Leisure', 'Savings & Investments', 'Miscellaneous'. Given following information: the annaul income is {input[2]}, the monthly rent/morgage is {input[3]}, {input[0]} is living in {input[6]} and {input[0]} has the following investment goals: planning to invest {input[5]} annaully and {input[7]}"}
        ],
        response_format={"type": "json_object"}
        
    )
    
    Budget = response.choices[0].message.content
    return Budget

# Use OpenAI API to execute code in a conversation
def Draw_Chart(JSON_DATA):
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"draw a horizotal barchart for following json object:{JSON_DATA}"
    )
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions=f"Please address the user as {user_input[0]}"
    )
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
        thread_id=thread.id
       )
    else:
      print(run.status)
    
    image_data = messages.data[0].content[0].image_file.file_id
    response = client.files.with_raw_response.content(image_data)
    if response.status_code == 200:
      image = Image.open(BytesIO(response.content))
      #return image
    else:
      st.write(f"failed to retrieve image.{response.status_code}")
      image = None
    return image
  

# Creating a button
if st.button("Submit"):

    st.write("\n", advise(user_input))
elif st.button("Monthly Budgeting Suggestion"):
    
    JSON_DATA=Suggest_Monthly_Budget(user_input)
    st.image(Draw_Chart(JSON_DATA), use_container_width=True)

    
