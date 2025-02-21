import streamlit as st
import openai
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
def Advise(input):
    client = openai.OpenAI(api_key= api)
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
           
            {"role": "user", "content": f"Please provide a {input[4]} fincial advice for {input[0]} who is {input[1]} years old: given following information: the annaul income is {input[2]}, the monthly rent/morgage is {input[3]}, {input[0]} is living in {input[6]} and {input[0]} has the following investment goals: planning to invest {input[5]} annaully and {input[7]}, also draw a \" Vertical Barchart \" for suggested monthly budget for {input[0]} including Housing (Rent/Mortgage & Utilities), Transportation, Groceries, Dining Out, Health & Insurance, Entertainment & Leisure, Savings & Investments, Miscellaneous."}
        ]
        
    )
    
    advise = response.choices[0].message.content
    return advise
    
def Suggest_Monthly_Budget(input):
    client = openai.OpenAI(api_key= api)
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
           
            {"role": "user", "content": f"Please suggest monthly budget for {input[0]} in JSON format who is {input[1]} years old containing following keys: 'Housing (Rent/Mortgage & Utilities)', 'Transportation', 'Groceries', 'Dining Out', 'Health & Insurance', 'Entertainment & Leisure', 'Savings & Investments', 'Miscellaneous'. Given following information: the annaul income is {input[2]}, the monthly rent/morgage is {input[3]}, {input[0]} is living in {input[6]} and {input[0]} has the following investment goals: planning to invest {input[5]} annaully and {input[7]}"}
        ],
        response_format={"type": "json_object"}
        
    )
    
    Budget = response.choices[0].message.content
    return Budget
    code = """
    x = sum(range(1, 101))
    x
    """

# Use OpenAI API to execute code in a conversation
def Draw_Chart(code):
    client = openai.OpenAI(api_key= api)
    response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a Python code execution assistant."},
        {"role": "user", "content": f"Execute this Python code and return the output:\n{code}"}
    ]
)
# Creating a button
if st.button("Your Finacial Advise"):
    print(user_input)

    st.write("\n", advise(user_input))

elif st.button("Monthly Budgeting Suggestion"):
    print(user_input)

    st.write("\n", Suggest_Monthly_Budget(user_input))
    st.write("\n", Draw_Chart(code))
    

    
