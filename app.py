from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import google.generativeai as genai
import PyPDF2

genai.configure(api_key=st.secrets["GOOGLE_API"])
# genai.configure(api_key="AIzaSyDSh_57xr9CeI2ZuTzHhzda-bRqDZm2N4k")



def get_gemini_response(input,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([input,prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file!=None:
        print(uploaded_file.read())
        text = ""
        with uploaded_file:
            # Create a PDF file reader object
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            
            # Loop through each page of the PDF
            for page_num in range(len(pdf_reader.pages)):
                # Extract text from the current page
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        print(text)
        return text
    else:
        return "No response Recorded"

## Streamlit App

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements job Description is:-:.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts job Description is:-:.
"""

input_prompt2 = """
You are a highly experienced career consultant with expertise in resume evaluation and job matching. Your task is to provide feedback and improvement tips based on the weaknesses identified in the resume, aligning it with the job description. Please share your professional evaluation and suggestions for improvement. Job improvements is:-:.
"""
st.set_page_config(page_title="Garuda ATS Resume EXpert")

# Set the default page to 1
current_page = 1

# Sidebar navigation
st.sidebar.image("garudaaihr.png",use_column_width=True)
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Go to", ("Garuda ATS Tracking System", "Garuda Conversation","UGC Mapping"))
uploaded_file = st.sidebar.file_uploader("Upload your resume(PDF)...",type=["pdf"])

# Page 1: Garuda ATS Tracking System
if page_selection == "Garuda ATS Tracking System":
    st.image("garuda.jpg", use_column_width=True)
    st.title("Garuda ATS Tracking System")
    input_text=st.text_area("Job Description: ",key="input")
    
    col2, col3, col4 = st.columns(3)

    with col2:
        submit1 = st.button("Resume Summary")

    with col3:
        submit2 = st.button("Improvements Suggestions")

    with col4:
        submit3 = st.button("Percentage match")
    
    if submit1:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt1+input_text,pdf_content)
            st.subheader("The Repsonse is")
            st.write(response)
            with open("response.txt", "w") as file:
                file.write(response)
                a = response
                download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
        else:
            st.write("Please upload the resume")

    elif submit2:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt2+input_text,pdf_content)
            st.subheader("The Repsonse is")
            st.write(response)
            with open("response.txt", "w") as file:
                file.write(response)
                a = response
                download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
        else:
            st.write("Please upload the resume")


    elif submit3:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_prompt3+input_text,pdf_content)
            st.subheader("The Repsonse is")
            st.write(response)
            with open("response.txt", "w") as file:
                file.write(response)
                a = response
                download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
        else:
            st.write("Please upload the resume")

# Page 2: Garuda Conversation
elif page_selection == "Garuda Conversation":
    st.image("phonix.jpg", use_column_width=True)
    st.title("Garuda Conversation")
    st.write("Ask your Question from the uploaded Resume ?")
    ip4 = "Please search "
    ip6 = "in the mentioned document and do not give any extra information give only those information which is mentioned in content as it is highly confidential information so only relevent information should be given"
    input_prompt4 = st.text_area("")
    submit4 = st.button("Search in Resume")
    response=""
    a=""
    if submit4:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(ip4+input_prompt4+ip6,pdf_content)
            st.subheader("The Repsonse is")
            st.write(response)
            with open("response.txt", "w") as file:
                file.write(response)
                a = response
                download_button = st.download_button("Download Response",a,file_name="Response.txt")

        else:
            st.write("Please upload the resume")
    

elif  page_selection == "UGC Mapping":
        st.image("groups.jpg", use_column_width=True)
        st.title("NORMS Matching System")
        input_text = st.text_area("Job Title: ", key="input")
        
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            
            # Read the UGC PDF file
            ugc_pdf_path = "ugc.pdf"  # Replace with the actual path to the UGC PDF file
            ugc_text = ""
            with open(ugc_pdf_path, "rb") as ugc_file:
                ugc_pdf_reader = PyPDF2.PdfReader(ugc_file)
                for page_num in range(len(ugc_pdf_reader.pages)):
                    page = ugc_pdf_reader.pages[page_num]
                    ugc_text += page.extract_text()
            
            input_prompt4 = "You are expert of university grant commission of India and I am giving you all the ugc text "
            
            # Generate response using Gemini
            submit6 = st.button("MAP")
            if submit6:
                    response = get_gemini_response(input_prompt4 + ugc_text + "Also I am providing you with the job to search in the text document and job title which you want to search in UGC norms is " +input_text, pdf_content)
                    st.subheader("HR Response")
                    st.write(response)
                    with open("response.txt", "w") as file:
                        file.write(response)
                        a = response
                        download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            

        else:
            st.write("Please upload the resume")


if uploaded_file is not None:
    st.sidebar.write("PDF Uploaded Successfully")



