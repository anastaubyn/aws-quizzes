import streamlit as st
import json
import random
import os

certificationCodes={
    'AI Practitioner': 'AIF-C01',
    'Cloud Practitioner': 'CLF-C02',
    'Machine Learning Engineer': 'MLA-C01',
    'Data Engineer': 'DEA-C01',
    'Developer': 'DVA-C02',
    'Solutions Architect Associate': 'SAA-C03',
    'SysOps Administrator': 'SOA-C02',
    'DevOps Engineer': 'DOP-C02',
    'Solutions Architect Professional': 'SAP-C02',
    'Advanced Networking Specialty': 'ANS-C01',
    'Machine Learning Specialty': 'MLS-C01',
    'Security Specialty': 'SCS-C02'
}

# Load the JSON file with questions
@st.cache_data
def load_questions(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        return None

# Main function to create the Streamlit app
def main():
    st.title("AWS Certification Preparation App")

    # Sidebar settings
    st.sidebar.header("Quiz Settings")
    
    cert_type = st.sidebar.selectbox(
        "Certification Code", certificationCodes.keys()
    )
    cert_code = certificationCodes[cert_type]
    st.image(f'images/{cert_code}.png', width=150, output_format='PNG')
    st.header(f"AWS {cert_type}")

    # Load questions
    questions = load_questions(f"{cert_code}.json")

    if questions is None:
        st.warning(f"No questions yet available for {cert_type}.")
        num_questions = 0
    else:
        if len(questions) == 1:
            num_questions = 1
        elif len(questions) < 10:
            num_questions = st.sidebar.slider(
                "Number of Questions", min_value=1, max_value=len(questions), value=len(questions)
            )
        else:
            num_questions = st.sidebar.slider(
                "Number of Questions", min_value=1, max_value=len(questions), value=10
            )

    if num_questions > 0:
        # Initialize session state for questions
        if "selected_questions" not in st.session_state or len(st.session_state.selected_questions) != num_questions:
            st.session_state.selected_questions = random.sample(questions, num_questions)

        # Display the quiz
        st.header("Take the Quiz")
        user_answers = {}
        for idx, question in enumerate(st.session_state.selected_questions):
            st.subheader(f"Question {idx + 1}")
            st.write(f"**{question['question']}**")
            options = question["answers"]
            
            # Handle multiple correct answers
            if len(question["correct_answer"]) > 1:
                user_answers[question["id"]] = st.multiselect(
                    f"Select {len(question['correct_answer'])} options for Question {idx + 1}:",
                    options,
                    key=f"q{idx}",
                    max_selections=len(question['correct_answer'])
                )
            else:
                user_answers[question["id"]] = st.radio(
                    f"Select your answer for Question {idx + 1}:", options, key=f"q{idx}"
                )
        # Regenerate Quiz Button
        if st.button("Restart"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
        # Submit button
        if st.button("Submit"):
            # Calculate score
            score = 0
            for question in st.session_state.selected_questions:
                if len(question['correct_answer']) == 1:
                    if user_answers[question["id"]] == question["correct_answer"][0]:
                        score += 1
                else:
                    if sorted(user_answers[question["id"]]) == sorted(question["correct_answer"]):
                        score += 1

            # Display results
            st.success(f"Quiz Completed! You scored {score}/{num_questions}.")

            # Show correct answers
            st.header("Correct Answers")
            for question in st.session_state.selected_questions:
                st.write(f"**{(question['question']).strip()}**")
                if len(question['correct_answer']) == 1:
                    if user_answers[question["id"]] == question["correct_answer"][0]:
                        st.success(f"{question["correct_answer"][0]}")
                    else:
                        st.error(f"{question["correct_answer"][0]}")
                else:
                    if sorted(user_answers[question["id"]]) == sorted(question["correct_answer"]):
                        for answer in question['correct_answer']:
                            st.success(f"{answer}")
                    else:
                        for answer in question['correct_answer']:
                            if answer in user_answers[question["id"]]:
                                st.success(f"{answer}")
                            else:
                                st.error(f"{answer}")

if __name__ == "__main__":
    main()
