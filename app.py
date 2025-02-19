import streamlit as st
import openai
st.title("Robo Advisor")
user_input= ['' for i in range(8)]
user_input[0] = st.text_input("Please enter your name:")
user_input[1] = st.text_input("Please enter your age:")
user_input[2] = st.text_input("Please enter your income:")
user_input[3] = st.text_input("Please enter your rent/morgage amount:")
user_input[4] = st.selectbox("Please enter your investment horizon:", ["Short term", "Medium term", "Long term"])
user_input[5] = st.text_input("Please enter your investment amount:")
user_input[6] = st.text_input("Please enter your location:")
user_input[7] = st.text_input("Please enter your investment goal:")

api = st.secrets["openai"]
def advise(input):
    client = openai.OpenAI(api_key= api)
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
           
            {"role": "user", "content": f"Please provide a {input[4]} fincial advice for {input[0]} who is {input[1]} years old: given following information: the annaul income is {input[2]}, the monthly rent/morgage is {input[3]}, {input[0]} is living in {input[6]} and {input[0]} has the following investment goals: planning to invest {input[5]} annaully and {input[7]}, also draw a bar chart to show suggested monthly budget for {input[0]} including Housing (Rent/Mortgage & Utilities), Transportation, Groceries, Dining Out, Health & Insurance, Entertainment & Leisure, Savings & Investments, Miscellaneous."}
        ]
        ]
    )
    
    advise = response.choices[0].message.content
    return advise
    

# Creating a button

if st.button("Submit"):
    print(user_input)

    st.write("\n", advise(user_input))
    
