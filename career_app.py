import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ═══════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════
st.set_page_config(page_title="Career Recommendation System", layout="wide")

st.title(" Career Recommendation System")
st.write("Fill in your profile and get a personalized career path recommendation backed by real student data.")

# ═══════════════════════════════════════════════
# LOAD DATASETS
# ═══════════════════════════════════════════════
df1 = pd.read_csv("Final_student_data.csv")
df1 = df1[df1['Program'] != 'Program'].copy()
df2 = pd.read_excel("updated_education_dataset.xlsx")

# ═══════════════════════════════════════════════
# SKILL → CAREER MAPPING
# ═══════════════════════════════════════════════
skill_career_map = {
    "python":              "Quantitative Analyst / Data Analyst",
    "sql":                 "Quantitative Analyst / Data Analyst",
    "r":                   "Quantitative Analyst / Data Analyst",
    "statistics":          "Quantitative Analyst / Data Analyst",
    "excel":               "Financial Analyst / Investment Analyst",
    "financial modelling": "Financial Analyst / Investment Analyst",
    "management":          "Portfolio Manager / Investment Strategist",
    "risk management":     "Risk Analyst / Risk Manager",
}

df1['Recommended Career'] = df1['Skill'].str.lower().map(skill_career_map).fillna("Financial Analyst / Investment Analyst")

# ═══════════════════════════════════════════════
# PROGRAM → CAREER MAPPING (df2)
# ═══════════════════════════════════════════════
program_career_map = {
    "BS Software Engineering":                              "Quantitative Analyst / Data Analyst",
    "BS Computer Science":                                  "Quantitative Analyst / Data Analyst",
    "BS Data Science":                                      "Quantitative Analyst / Data Analyst",
    "BS Artificial Intelligence":                           "Quantitative Analyst / Data Analyst",
    "BS Information Technology":                            "Quantitative Analyst / Data Analyst",
    "BS Financial Engineering / BS Computational Finance":  "Quantitative Analyst / Data Analyst",
    "BS Cyber Security":                                    "Risk Analyst / Risk Manager",
    "BS Accounting & Finance":                              "Financial Analyst / Investment Analyst",
    "BS Business Analytics":                                "Financial Analyst / Investment Analyst",
    "BBA (Bachelor of Business Administration)":            "Financial Analyst / Investment Analyst",
    "BBA":                                                  "Financial Analyst / Investment Analyst",
    "BS Economics":                                         "Financial Analyst / Investment Analyst",
    "BS Marketing":                                         "Portfolio Manager / Investment Strategist",
    "BS Entrepreneurship":                                  "Portfolio Manager / Investment Strategist",
    "BS Human Resource Management":                         "Portfolio Manager / Investment Strategist",
}
df2['Recommended Career'] = df2['Program'].map(program_career_map).fillna("Financial Analyst / Investment Analyst")

# ═══════════════════════════════════════════════
# RECOMMENDATION FUNCTION
# ═══════════════════════════════════════════════
def recommend_career(student):
    skills = [s.strip().lower() for s in student['Skills']] if isinstance(student['Skills'], list) else [student['Skills'].strip().lower()]

    career_scores = {
        "Quantitative Analyst / Data Analyst":      0,
        "Financial Analyst / Investment Analyst":    0,
        "Risk Analyst / Risk Manager":               0,
        "Portfolio Manager / Investment Strategist": 0,
    }

    for s in skills:
        target = skill_career_map.get(s)
        if target and target in career_scores:
            career_scores[target] += 15

    cgpa    = float(student.get('CGPA', 0))
    soft    = float(student.get('Soft Skills Score', 5))
    interns = int(student.get('Internships', 0))
    certs   = int(student.get('Certifications', 0))
    projs   = int(student.get('Projects', 0))

    for c in career_scores:
        career_scores[c] += cgpa * 2
        career_scores[c] += soft * 1.5
        career_scores[c] += interns * 1.5
        career_scores[c] += certs * 1
        career_scores[c] += projs * 0.5

    recommended = max(career_scores, key=career_scores.get)

    edu_map = {
        "Quantitative Analyst / Data Analyst":      "Masters in Financial Engineering / Data Science",
        "Financial Analyst / Investment Analyst":    "MBA in Finance / CFA",
        "Risk Analyst / Risk Manager":               "Masters in Risk Management / FRM",
        "Portfolio Manager / Investment Strategist": "Masters in Finance / CFA",
    }

    job_map = {
        "Quantitative Analyst / Data Analyst": [
            "Data Analyst at a Bank or Financial Institution",
            "Quantitative Analyst at a Hedge Fund",
            "Business Intelligence Analyst at a FinTech Firm",
            "Credit Risk Data Analyst at an Insurance Company",
            "Research Analyst at an Investment Firm",
        ],
        "Financial Analyst / Investment Analyst": [
            "Financial Analyst at a Corporate Finance Department",
            "Investment Analyst at a Brokerage Firm",
            "Equity Research Analyst at an Asset Management Company",
            "Budget Analyst at a Multinational Corporation",
            "Valuation Analyst at a Consulting Firm",
        ],
        "Risk Analyst / Risk Manager": [
            "Credit Risk Analyst at a Commercial Bank",
            "Market Risk Analyst at an Investment Bank",
            "Operational Risk Manager at an Insurance Firm",
            "Compliance Risk Analyst at a Regulatory Body",
            "Enterprise Risk Consultant at a Big-4 Firm",
        ],
        "Portfolio Manager / Investment Strategist": [
            "Portfolio Manager at a Mutual Fund Company",
            "Wealth Manager at a Private Bank",
            "Investment Strategist at a Family Office",
            "Fund Analyst at a Pension Fund",
            "Asset Allocation Analyst at an Insurance Firm",
        ],
    }

    return recommended, edu_map[recommended], job_map[recommended], career_scores

# ═══════════════════════════════════════════════
# INPUT FORM
# ═══════════════════════════════════════════════
INSTITUTES = [
    "Ned Universty of Engineering and Technology",
    "IBA — Institute of Business Administration",
    "FAST — National University",
    "LUMS — Lahore University of Management Sciences",
    "NUST — National University of Sciences & Technology",
    "UET — University of Engineering & Technology",
    "Karachi University",
    "Punjab University",
    "Aga Khan University",
    "COMSATS University",
    "Other",
]

st.header(" Student Profile")

with st.form("career_form"):
    col_a, col_b = st.columns(2)

    with col_a:
        name   = st.text_input("Full Name")
        age    = st.number_input("Age", min_value=15, max_value=40)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        base_programs = [p for p in df1['Program'].dropna().unique().tolist()
                         if p not in ['BS Computational Finance']]
        program_options = sorted(base_programs) + ["BS Computational Finance"]
        program = st.selectbox("Program", program_options)

        # ── Institution input — sits in the empty space below Program ──
        institution = st.selectbox("Institution", INSTITUTES)

    with col_b:
        cgpa        = st.number_input("CGPA (out of 4.0)", min_value=0.0, max_value=4.0, step=0.01)
        internships = st.number_input("Internships Completed", min_value=0, max_value=10)
        projects    = st.number_input("Projects Completed", min_value=0, max_value=20)
        certs       = st.number_input("Certifications", min_value=0, max_value=10)
        soft_skills = st.slider("Soft Skills Score (1–10)", 1, 10, 5)

    skills = st.multiselect(
        "Select Your Skills",
        ["Python", "R", "SQL", "Statistics",
         "Excel", "Financial Modelling",
         "Risk Management", "Management"]
    )

    submit = st.form_submit_button("🔍 Get My Career Recommendation")


# ═══════════════════════════════════════════════
# RESULT + CONFIDENCE + DASHBOARD
# ═══════════════════════════════════════════════
if submit:

    if name.strip() == "" or len(skills) == 0 or cgpa == 0.0:
        st.error(" Please fill in your Name, CGPA, and at least one Skill.")

    else:
        student_input = {
            'Skills':            skills,
            'CGPA':              cgpa,
            'Soft Skills Score': soft_skills,
            'Internships':       internships,
            'Projects':          projects,
            'Certifications':    certs,
        }

        career, edu, jobs, scores = recommend_career(student_input)

        # ── RESULT SECTION ───────────────────────────────────
        st.divider()
        st.header(" Your Result")

        res1, res2 = st.columns([1.2, 1])

        with res1:
            st.success(f"**Recommended Career:** {career}")
            st.info(f" **Suggested Further Education:** {edu}")
            st.caption(f" Institution: {institution}  |  📘 Program: {program}")
            st.subheader(" Recommended Job Titles")
            for i, job in enumerate(jobs, 1):
                st.markdown(f"**{i}.** {job}")

        with res2:
            cats = list(scores.keys())
            vals = list(scores.values())
            radar = go.Figure(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=cats + [cats[0]],
                fill='toself',
                line_color='royalblue',
                fillcolor='rgba(65,105,225,0.2)'
            ))
            radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, showticklabels=False)),
                title=f"{name}'s Career Score Breakdown",
                showlegend=False,
                margin=dict(t=50, b=10, l=20, r=20),
                height=320
            )
            st.plotly_chart(radar, use_container_width=True)

        # ── CONFIDENCE % SECTION ─────────────────────────────
        # To remove: delete from here to END CONFIDENCE
        st.divider()
        st.subheader(" Career Match Confidence")

        total_score = sum(scores.values())
        for career_name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            pct = int((score / total_score) * 100) if total_score > 0 else 0
            is_top = career_name == career
            label = f"{'✅ ' if is_top else ''}{career_name}  —  **{pct}% match**"
            st.markdown(label)
            st.progress(pct / 100)
        # ── END CONFIDENCE ───────────────────────────────────

        # ── DASHBOARD SECTION ────────────────────────────────
        st.divider()
        st.header(" Dashboard — Student Dataset Insights")

        career_counts  = df1['Recommended Career'].value_counts().reset_index()
        career_counts.columns  = ['Career', 'Count']

        skill_counts   = df1['Skill'].value_counts().reset_index()
        skill_counts.columns   = ['Skill', 'Count']

        program_counts = df1['Program'].value_counts().reset_index()
        program_counts.columns = ['Program', 'Count']

        # Row 1 — Key Metrics
        st.subheader(" Key Metrics")
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total Students",       f"{len(df1):,}")
        k2.metric("Average CGPA",          f"{df1['CGPA'].mean():.2f}")
        k3.metric("Top Skill",             skill_counts.iloc[0]['Skill'])
        k4.metric("Top Career Path",       career_counts.iloc[0]['Career'].split("/")[0].strip())
        k5.metric("Avg Internships (df2)", f"{df2['Internships_Completed'].mean():.1f}")

        # Row 2 — Career Distribution
        st.subheader(" Career Distribution ")
        g1, g2 = st.columns(2)

        with g1:
            bar = px.bar(
                career_counts, x='Career', y='Count',
                color='Career', text='Count',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            bar.update_layout(showlegend=False, xaxis_tickangle=-15,
                              xaxis_title="", yaxis_title="No. of Students")
            bar.update_traces(textposition='outside')
            st.plotly_chart(bar, use_container_width=True)

        with g2:
            pie = px.pie(
                career_counts, names='Career', values='Count',
                hole=0.42,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            pie.update_traces(textposition='inside', textinfo='percent+label')
            pie.update_layout(showlegend=False)
            st.plotly_chart(pie, use_container_width=True)

        # Row 3 — Skills + Program
        st.subheader(" Skills & Program Distribution")
        g3, g4 = st.columns(2)

        with g3:
            skill_bar = px.bar(
                skill_counts, x='Skill', y='Count',
                color='Skill', text='Count',
                title="Skill-wise Student Count",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            skill_bar.update_layout(showlegend=False, xaxis_tickangle=-15, xaxis_title="")
            skill_bar.update_traces(textposition='outside')
            st.plotly_chart(skill_bar, use_container_width=True)

        with g4:
            prog_pie = px.pie(
                program_counts, names='Program', values='Count',
                hole=0.35,
                title="Students by Program",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            prog_pie.update_traces(textposition='inside', textinfo='percent')
            prog_pie.update_layout(showlegend=True, legend=dict(font=dict(size=10)))
            st.plotly_chart(prog_pie, use_container_width=True)

        # # Row 4 — CGPA by Career
        # st.subheader(" CGPA Distribution by Career Path")
        # cgpa_box = px.box(
        #     df1, x='Recommended Career', y='CGPA',
        #     color='Recommended Career',
        #     color_discrete_sequence=px.colors.qualitative.Bold
        # )
        # cgpa_box.update_layout(showlegend=False, xaxis_title="", xaxis_tickangle=-10)
        # st.plotly_chart(cgpa_box, use_container_width=True)

        # Row 5 — df2 Insights
        st.subheader(" Education Dataset Insights")
        e1, e2, e3 = st.columns(3)

        with e1:
            intern_bar = px.bar(
                df2['Internships_Completed'].value_counts().reset_index().rename(
                    columns={'Internships_Completed': 'Internships', 'count': 'Count'}),
                x='Internships', y='Count',
                color='Internships', text='Count',
                title="Internships Completed",
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            intern_bar.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(intern_bar, use_container_width=True)

        with e2:
            edu_pie = px.pie(
                df2['Further_Education_Plans'].value_counts().reset_index().rename(
                    columns={'Further_Education_Plans': 'Plan', 'count': 'Count'}),
                names='Plan', values='Count',
                hole=0.4,
                title="Further Education Plans",
                color_discrete_sequence=px.colors.qualitative.Antique
            )
            edu_pie.update_traces(textposition='inside', textinfo='percent+label')
            edu_pie.update_layout(showlegend=False)
            st.plotly_chart(edu_pie, use_container_width=True)

        with e3:
            cert_bar = px.bar(
                df2['Certifications'].value_counts().reset_index().rename(
                    columns={'Certifications': 'Certs', 'count': 'Count'}),
                x='Certs', y='Count',
                color='Certs', text='Count',
                title="Certifications Earned",
                color_discrete_sequence=px.colors.sequential.Teal
            )
            cert_bar.update_layout(showlegend=False, coloraxis_showscale=False,
                                   xaxis_title="No. of Certifications")
            st.plotly_chart(cert_bar, use_container_width=True)