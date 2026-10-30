
import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title = "Student CGPA Calculator",
    page_icon = "🎓",      #windows + . to access emoji collection on pc
    layout = "centered"
)

# Grading System
grade_points = {
    "A": 4,
    "B": 3,
    "C": 2,
    "D": 1,
    "E": 0,
}

# Application Title
st.title("🎓 Student CGPA Calculator")

st.write(
    "Calculate your CGPA using your course credit units and grades."
)

st.info("This calculator uses a 4.00 grading scale")

# Course input
st.subheader("Enter Course Details")

number_of_courses = st.number_input(
    "Number of courses",
    min_value=1,
    max_value=30,
    value=2,   #default number to be showed
    step=1  #the number of times it should be increased
)

courses = []

for i in range(int(number_of_courses)):
    st.markdown(f"### Course {i + 1}")

    col1, col2, col3 = st.columns(3)

    with col1:
        course_code = st.text_input(
            "Course Code", 
            key=f"code_{i}"
        )

    with col2:
        credit_unit = st.number_input(
            "Credit Unit",
            min_value=1,
            max_value=4,
            value=2,
            key=f"unit_{i}"
        )

    with col3:
        grade = st.selectbox(
            "Grade",
            options=["A", "B", "C", "D", "E"],
            key=f"grade_{i}"
        )

    courses.append({
        "Course Code": course_code,
        "Credit Unit": credit_unit,
        "Grade": grade
    })

# Calculate button
if st.button("Calculate CGPA", type="primary"):     #primary refers to the colour of the  button...

    total_credit_units = 0
    total_quality_points = 0

    results = []

    for course in courses:

        grade_point = grade_points[course["Grade"]]

        quality_point = (
            course["Credit Unit"]*grade_point
        )

        total_credit_units += course["Credit Unit"]
        total_quality_points += quality_point

        results.append({
            "Course Code": course["Course Code"],
            "Credit Unit": course["Credit Unit"],
            "Grade": course["Grade"],
            "Grade Point": grade_point,
            "Quality Point": quality_point
        })

    cgpa = total_quality_points / total_credit_units

# Display results
    st.success("CGPA calculated successfully!")

    st.subheader("Academic Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Units",
        total_credit_units
    )

    col2.metric(
        "Quality Points",
        total_quality_points
    )

    col3.metric(
        "CGPA",
        f"{cgpa:2f} / 4.00"
    )

# Display course table
    st.subheader("Course Breakdown")

    results_df = pd.DataFrame(results)

    st.dataframe(
        results_df,
        use_container_width=True,    #wideness of the table
        hide_index=True
    )

# Download results
    csv = results_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Result",
        data=csv,
        file_name="student_cgpa_result.csv",
        mime="text/csv"
    )
