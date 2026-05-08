# ============================================================
# EDWISERR — Career Profiles Dataset (Expanded)
# 100+ careers: O*NET (global) + Indian careers layer
#
# Refactored:
#   - Normalized OCEAN values (20–90 range)
#   - Trait weights added (sum to 1.0)
#   - Standardized work_style vocabulary
#   - Schema validation at module load
# ============================================================

# ── CONSTANTS ────────────────────────────────────────────────

REQUIRED_TRAITS = [
    "Openness",
    "Conscientiousness",
    "Extraversion",
    "Agreeableness",
    "Neuroticism",
]

VALID_SOURCES = {"onet", "indian", "hybrid"}

STANDARD_WORK_STYLES = {
    "analytical",
    "creative",
    "leadership",
    "collaborative",
    "independent",
    "technical",
    "research",
    "social",
    "structured",
    "hands_on",
    "communication",
    "problem_solving",
    "strategic",
    "artistic",
    "caregiving",
    "entrepreneurial",
}


# ── CAREER PROFILES ──────────────────────────────────────────

CAREERS = [

    # ── TECHNOLOGY & DATA ────────────────────────────────────

    {
        "id": "data_scientist",
        "name": "Data Scientist",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Analyse complex datasets to extract insights and build predictive models.",
        "ocean_profile": {
            "Openness": 82, "Conscientiousness": 80, "Extraversion": 38,
            "Agreeableness": 52, "Neuroticism": 25,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.30, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["analytical", "independent", "technical"],
    },

    {
        "id": "software_engineer",
        "name": "Software Engineer",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Design, build and maintain software systems and applications.",
        "ocean_profile": {
            "Openness": 70, "Conscientiousness": 82, "Extraversion": 40,
            "Agreeableness": 52, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.35, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "JEE (for CS degree pathway)",
        "work_style": ["technical", "structured", "problem_solving"],
    },

    {
        "id": "ml_engineer",
        "name": "Machine Learning Engineer",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Build and deploy ML models and AI systems at scale.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 84, "Extraversion": 36,
            "Agreeableness": 48, "Neuroticism": 25,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.35, "Extraversion": 0.10,
            "Agreeableness": 0.10, "Neuroticism": 0.20,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["analytical", "technical", "problem_solving"],
    },

    {
        "id": "ai_researcher",
        "name": "AI Researcher",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Conduct cutting-edge research in artificial intelligence and machine learning.",
        "ocean_profile": {
            "Openness": 88, "Conscientiousness": 78, "Extraversion": 32,
            "Agreeableness": 50, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.35, "Conscientiousness": 0.30, "Extraversion": 0.08,
            "Agreeableness": 0.12, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["research", "analytical", "independent"],
    },

    {
        "id": "cybersecurity_analyst",
        "name": "Cybersecurity Analyst",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Protect systems and networks from digital threats and attacks.",
        "ocean_profile": {
            "Openness": 65, "Conscientiousness": 88, "Extraversion": 36,
            "Agreeableness": 45, "Neuroticism": 25,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.40, "Extraversion": 0.10,
            "Agreeableness": 0.10, "Neuroticism": 0.25,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["analytical", "technical", "independent"],
    },

    {
        "id": "devops_engineer",
        "name": "DevOps Engineer",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Bridge development and operations to streamline software delivery pipelines.",
        "ocean_profile": {
            "Openness": 68, "Conscientiousness": 85, "Extraversion": 42,
            "Agreeableness": 56, "Neuroticism": 26,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.35, "Extraversion": 0.15,
            "Agreeableness": 0.20, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["technical", "structured", "collaborative"],
    },

    {
        "id": "cloud_architect",
        "name": "Cloud Architect",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Design and manage cloud infrastructure for organisations at scale.",
        "ocean_profile": {
            "Openness": 72, "Conscientiousness": 86, "Extraversion": 44,
            "Agreeableness": 50, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.35, "Extraversion": 0.15,
            "Agreeableness": 0.10, "Neuroticism": 0.20,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["technical", "strategic", "structured"],
    },

    {
        "id": "ux_designer",
        "name": "UX/UI Designer",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Design intuitive, user-centred digital interfaces and experiences.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 65, "Extraversion": 58,
            "Agreeableness": 72, "Neuroticism": 35,
        },
        "weights": {
            "Openness": 0.35, "Conscientiousness": 0.15, "Extraversion": 0.20,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["creative", "collaborative", "analytical"],
    },

    {
        "id": "product_manager",
        "name": "Product Manager",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Lead product vision, strategy and cross-functional execution.",
        "ocean_profile": {
            "Openness": 76, "Conscientiousness": 78, "Extraversion": 70,
            "Agreeableness": 65, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.25, "Extraversion": 0.25,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["strategic", "communication", "leadership"],
    },

    {
        "id": "blockchain_developer",
        "name": "Blockchain Developer",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Build decentralised applications and smart contracts on blockchain platforms.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 80, "Extraversion": 35,
            "Agreeableness": 48, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.35, "Extraversion": 0.08,
            "Agreeableness": 0.12, "Neuroticism": 0.20,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["technical", "analytical", "independent"],
    },

    {
        "id": "data_engineer",
        "name": "Data Engineer",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Build and maintain data pipelines and infrastructure for analytics teams.",
        "ocean_profile": {
            "Openness": 65, "Conscientiousness": 86, "Extraversion": 38,
            "Agreeableness": 52, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.40, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.20,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["technical", "structured", "analytical"],
    },

    {
        "id": "game_developer",
        "name": "Game Developer",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Design and build interactive games for mobile, PC and console platforms.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 70, "Extraversion": 45,
            "Agreeableness": 55, "Neuroticism": 32,
        },
        "weights": {
            "Openness": 0.35, "Conscientiousness": 0.25, "Extraversion": 0.15,
            "Agreeableness": 0.10, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["creative", "technical", "problem_solving"],
    },

    {
        "id": "it_consultant",
        "name": "IT Consultant",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Advise organisations on technology strategy and digital transformation.",
        "ocean_profile": {
            "Openness": 72, "Conscientiousness": 78, "Extraversion": 68,
            "Agreeableness": 62, "Neuroticism": 26,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.25, "Extraversion": 0.25,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["strategic", "communication", "analytical"],
    },

    # ── RESEARCH & ACADEMIA ──────────────────────────────────

    {
        "id": "research_scientist",
        "name": "Research Scientist",
        "category": "Research & Academia",
        "source": "onet",
        "description": "Conduct original research to advance knowledge in a scientific field.",
        "ocean_profile": {
            "Openness": 88, "Conscientiousness": 80, "Extraversion": 32,
            "Agreeableness": 52, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.35, "Conscientiousness": 0.30, "Extraversion": 0.08,
            "Agreeableness": 0.12, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "GATE / CSIR-NET / JEST",
        "work_style": ["analytical", "research", "independent"],
    },

    {
        "id": "university_professor",
        "name": "University Professor",
        "category": "Research & Academia",
        "source": "hybrid",
        "description": "Teach, mentor students and conduct research at a university.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 75, "Extraversion": 62,
            "Agreeableness": 68, "Neuroticism": 26,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.20, "Extraversion": 0.25,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UGC-NET / PhD",
        "work_style": ["research", "communication", "independent"],
    },

    {
        "id": "data_analyst",
        "name": "Data Analyst",
        "category": "Research & Academia",
        "source": "onet",
        "description": "Interpret data and generate actionable business insights.",
        "ocean_profile": {
            "Openness": 68, "Conscientiousness": 82, "Extraversion": 42,
            "Agreeableness": 55, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.35, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["analytical", "structured", "research"],
    },

    {
        "id": "statistician",
        "name": "Statistician",
        "category": "Research & Academia",
        "source": "onet",
        "description": "Apply statistical methods to collect, analyse and interpret data.",
        "ocean_profile": {
            "Openness": 68, "Conscientiousness": 86, "Extraversion": 34,
            "Agreeableness": 52, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.40, "Extraversion": 0.08,
            "Agreeableness": 0.12, "Neuroticism": 0.20,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "CSIR-NET (Statistics)",
        "work_style": ["analytical", "structured", "independent"],
    },

    {
        "id": "economist",
        "name": "Economist",
        "category": "Research & Academia",
        "source": "onet",
        "description": "Study production, distribution and consumption of goods and services.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 76, "Extraversion": 48,
            "Agreeableness": 52, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.25, "Extraversion": 0.15,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "IES / RBI Grade B",
        "work_style": ["analytical", "research", "structured"],
    },

    {
        "id": "historian",
        "name": "Historian / Archivist",
        "category": "Research & Academia",
        "source": "onet",
        "description": "Research and document historical events, cultures and societies.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 78, "Extraversion": 36,
            "Agreeableness": 60, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.40, "Conscientiousness": 0.25, "Extraversion": 0.08,
            "Agreeableness": 0.15, "Neuroticism": 0.12,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UGC-NET History",
        "work_style": ["research", "analytical", "independent"],
    },

    # ── MEDICINE & HEALTH ────────────────────────────────────

    {
        "id": "doctor_mbbs",
        "name": "Medical Doctor (MBBS)",
        "category": "Medicine & Health",
        "source": "indian",
        "description": "Diagnose and treat patients across clinical settings.",
        "ocean_profile": {
            "Openness": 65, "Conscientiousness": 88, "Extraversion": 58,
            "Agreeableness": 78, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.35, "Extraversion": 0.15,
            "Agreeableness": 0.25, "Neuroticism": 0.10,
        },
        "user_types": ["class_10", "class_12"],
        "entrance_exam": "NEET-UG",
        "work_style": ["caregiving", "structured", "problem_solving"],
    },

    {
        "id": "surgeon",
        "name": "Surgeon",
        "category": "Medicine & Health",
        "source": "onet",
        "description": "Perform surgical procedures to treat disease, injury and deformity.",
        "ocean_profile": {
            "Openness": 58, "Conscientiousness": 90, "Extraversion": 50,
            "Agreeableness": 55, "Neuroticism": 20,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.45, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.20,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "NEET-PG / MS",
        "work_style": ["technical", "hands_on", "structured"],
    },

    {
        "id": "psychiatrist",
        "name": "Psychiatrist",
        "category": "Medicine & Health",
        "source": "onet",
        "description": "Diagnose and treat mental health disorders using therapy and medication.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 76, "Extraversion": 55,
            "Agreeableness": 84, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.20, "Extraversion": 0.15,
            "Agreeableness": 0.30, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "NEET-PG / MD Psychiatry",
        "work_style": ["caregiving", "analytical", "research"],
    },

    {
        "id": "physiotherapist",
        "name": "Physiotherapist",
        "category": "Medicine & Health",
        "source": "hybrid",
        "description": "Rehabilitate patients with physical impairments through exercise and therapy.",
        "ocean_profile": {
            "Openness": 60, "Conscientiousness": 76, "Extraversion": 64,
            "Agreeableness": 84, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.25, "Extraversion": 0.20,
            "Agreeableness": 0.35, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NEET / BPT entrance",
        "work_style": ["hands_on", "caregiving", "collaborative"],
    },

    {
        "id": "dentist",
        "name": "Dentist",
        "category": "Medicine & Health",
        "source": "indian",
        "description": "Diagnose and treat conditions affecting teeth, gums and oral health.",
        "ocean_profile": {
            "Openness": 58, "Conscientiousness": 86, "Extraversion": 55,
            "Agreeableness": 74, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.40, "Extraversion": 0.15,
            "Agreeableness": 0.25, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NEET-UG (BDS)",
        "work_style": ["technical", "caregiving", "hands_on"],
    },

    {
        "id": "public_health_specialist",
        "name": "Public Health Specialist",
        "category": "Medicine & Health",
        "source": "hybrid",
        "description": "Design and implement health programmes at community or national scale.",
        "ocean_profile": {
            "Openness": 74, "Conscientiousness": 74, "Extraversion": 65,
            "Agreeableness": 80, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.20, "Extraversion": 0.20,
            "Agreeableness": 0.30, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "MPH entrance / UPSC",
        "work_style": ["strategic", "collaborative", "caregiving"],
    },

    {
        "id": "radiologist",
        "name": "Radiologist",
        "category": "Medicine & Health",
        "source": "onet",
        "description": "Interpret medical images to diagnose and guide treatment of disease.",
        "ocean_profile": {
            "Openness": 62, "Conscientiousness": 88, "Extraversion": 38,
            "Agreeableness": 58, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.45, "Extraversion": 0.08,
            "Agreeableness": 0.15, "Neuroticism": 0.17,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "NEET-PG / MD Radiology",
        "work_style": ["analytical", "technical", "independent"],
    },

    {
        "id": "nurse",
        "name": "Nurse / Nursing Officer",
        "category": "Medicine & Health",
        "source": "indian",
        "description": "Provide direct patient care and coordinate health services in clinical settings.",
        "ocean_profile": {
            "Openness": 58, "Conscientiousness": 82, "Extraversion": 64,
            "Agreeableness": 88, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.25, "Extraversion": 0.20,
            "Agreeableness": 0.35, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "B.Sc Nursing / AIIMS Nursing",
        "work_style": ["caregiving", "collaborative", "hands_on"],
    },

    {
        "id": "nutritionist",
        "name": "Dietitian / Nutritionist",
        "category": "Medicine & Health",
        "source": "onet",
        "description": "Advise individuals and organisations on diet, nutrition and healthy eating.",
        "ocean_profile": {
            "Openness": 62, "Conscientiousness": 76, "Extraversion": 60,
            "Agreeableness": 78, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.25, "Extraversion": 0.20,
            "Agreeableness": 0.30, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["caregiving", "structured", "communication"],
    },

    # ── ENGINEERING ──────────────────────────────────────────

    {
        "id": "civil_engineer",
        "name": "Civil Engineer",
        "category": "Engineering",
        "source": "hybrid",
        "description": "Design and oversee construction of infrastructure — roads, bridges, buildings.",
        "ocean_profile": {
            "Openness": 58, "Conscientiousness": 85, "Extraversion": 50,
            "Agreeableness": 58, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.40, "Extraversion": 0.15,
            "Agreeableness": 0.20, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE Main / JEE Advanced",
        "work_style": ["structured", "hands_on", "leadership"],
    },

    {
        "id": "mechanical_engineer",
        "name": "Mechanical Engineer",
        "category": "Engineering",
        "source": "hybrid",
        "description": "Design and analyse mechanical systems, machines and thermal devices.",
        "ocean_profile": {
            "Openness": 62, "Conscientiousness": 84, "Extraversion": 44,
            "Agreeableness": 52, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.40, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE Main / JEE Advanced",
        "work_style": ["technical", "structured", "problem_solving"],
    },

    {
        "id": "electrical_engineer",
        "name": "Electrical Engineer",
        "category": "Engineering",
        "source": "hybrid",
        "description": "Design and develop electrical systems, circuits and power infrastructure.",
        "ocean_profile": {
            "Openness": 65, "Conscientiousness": 84, "Extraversion": 40,
            "Agreeableness": 50, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.40, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE Main / GATE",
        "work_style": ["analytical", "technical", "structured"],
    },

    {
        "id": "aerospace_engineer",
        "name": "Aerospace Engineer",
        "category": "Engineering",
        "source": "onet",
        "description": "Design aircraft, spacecraft and related systems.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 88, "Extraversion": 40,
            "Agreeableness": 50, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.40, "Extraversion": 0.10,
            "Agreeableness": 0.10, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE Advanced / IIST entrance",
        "work_style": ["technical", "analytical", "problem_solving"],
    },

    {
        "id": "chemical_engineer",
        "name": "Chemical Engineer",
        "category": "Engineering",
        "source": "onet",
        "description": "Design processes for producing, transforming and transporting chemicals.",
        "ocean_profile": {
            "Openness": 68, "Conscientiousness": 84, "Extraversion": 42,
            "Agreeableness": 52, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.40, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE Main / JEE Advanced",
        "work_style": ["analytical", "structured", "technical"],
    },

    {
        "id": "robotics_engineer",
        "name": "Robotics Engineer",
        "category": "Engineering",
        "source": "onet",
        "description": "Design, build and program robotic systems for automation and research.",
        "ocean_profile": {
            "Openness": 80, "Conscientiousness": 84, "Extraversion": 38,
            "Agreeableness": 50, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.35, "Extraversion": 0.08,
            "Agreeableness": 0.12, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "JEE / GATE (ME/EE)",
        "work_style": ["technical", "analytical", "problem_solving"],
    },

    {
        "id": "environmental_engineer",
        "name": "Environmental Engineer",
        "category": "Engineering",
        "source": "onet",
        "description": "Develop solutions to environmental problems like pollution and waste management.",
        "ocean_profile": {
            "Openness": 74, "Conscientiousness": 78, "Extraversion": 50,
            "Agreeableness": 68, "Neuroticism": 26,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.30, "Extraversion": 0.15,
            "Agreeableness": 0.25, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE / GATE (ENV)",
        "work_style": ["analytical", "structured", "hands_on"],
    },

    {
        "id": "petroleum_engineer",
        "name": "Petroleum Engineer",
        "category": "Engineering",
        "source": "onet",
        "description": "Design methods for extracting oil and gas from the earth efficiently.",
        "ocean_profile": {
            "Openness": 62, "Conscientiousness": 84, "Extraversion": 48,
            "Agreeableness": 50, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.40, "Extraversion": 0.15,
            "Agreeableness": 0.15, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE / ONGC recruitment",
        "work_style": ["technical", "hands_on", "analytical"],
    },

    {
        "id": "textile_engineer",
        "name": "Textile Engineer",
        "category": "Engineering",
        "source": "indian",
        "description": "Develop and improve fibres, yarns, fabrics and textile processes.",
        "ocean_profile": {
            "Openness": 60, "Conscientiousness": 80, "Extraversion": 44,
            "Agreeableness": 55, "Neuroticism": 26,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.40, "Extraversion": 0.10,
            "Agreeableness": 0.20, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE / NIFT (technical)",
        "work_style": ["technical", "structured", "analytical"],
    },

    # ── BUSINESS & FINANCE ───────────────────────────────────

    {
        "id": "chartered_accountant",
        "name": "Chartered Accountant (CA)",
        "category": "Business & Finance",
        "source": "indian",
        "description": "Manage financial reporting, auditing and taxation for organisations.",
        "ocean_profile": {
            "Openness": 48, "Conscientiousness": 90, "Extraversion": 44,
            "Agreeableness": 55, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.08, "Conscientiousness": 0.50, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.17,
        },
        "user_types": ["class_10", "class_12", "undergraduate"],
        "entrance_exam": "CA Foundation / ICAI",
        "work_style": ["analytical", "structured", "independent"],
    },

    {
        "id": "investment_banker",
        "name": "Investment Banker",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Raise capital, execute M&A deals and advise corporations on financial strategy.",
        "ocean_profile": {
            "Openness": 65, "Conscientiousness": 86, "Extraversion": 72,
            "Agreeableness": 48, "Neuroticism": 25,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.30, "Extraversion": 0.30,
            "Agreeableness": 0.10, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "CAT / CFA / MBA",
        "work_style": ["analytical", "strategic", "leadership"],
    },

    {
        "id": "financial_analyst",
        "name": "Financial Analyst",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Evaluate financial data to support investment and business decisions.",
        "ocean_profile": {
            "Openness": 62, "Conscientiousness": 84, "Extraversion": 46,
            "Agreeableness": 52, "Neuroticism": 26,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.40, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "CFA / MBA Finance",
        "work_style": ["analytical", "structured", "research"],
    },

    {
        "id": "entrepreneur",
        "name": "Entrepreneur",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Build and scale a business from idea to execution.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 70, "Extraversion": 76,
            "Agreeableness": 58, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.20, "Extraversion": 0.25,
            "Agreeableness": 0.10, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["entrepreneurial", "leadership", "strategic"],
    },

    {
        "id": "management_consultant",
        "name": "Management Consultant",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Solve complex business problems and advise organisations on strategy.",
        "ocean_profile": {
            "Openness": 76, "Conscientiousness": 80, "Extraversion": 72,
            "Agreeableness": 60, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.25, "Extraversion": 0.25,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "CAT / GMAT / MBA",
        "work_style": ["analytical", "communication", "strategic"],
    },

    {
        "id": "actuary",
        "name": "Actuary",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Use mathematics and statistics to assess financial risk.",
        "ocean_profile": {
            "Openness": 65, "Conscientiousness": 88, "Extraversion": 36,
            "Agreeableness": 50, "Neuroticism": 20,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.45, "Extraversion": 0.08,
            "Agreeableness": 0.12, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "IAI / IFoA actuarial exams",
        "work_style": ["analytical", "structured", "independent"],
    },

    {
        "id": "marketing_manager",
        "name": "Marketing Manager",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Develop and execute marketing strategies to grow brand and revenue.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 70, "Extraversion": 78,
            "Agreeableness": 65, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.15, "Extraversion": 0.30,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "CAT / MBA Marketing",
        "work_style": ["creative", "strategic", "communication"],
    },

    {
        "id": "hr_manager",
        "name": "Human Resources Manager",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Manage talent acquisition, development and employee relations.",
        "ocean_profile": {
            "Openness": 65, "Conscientiousness": 74, "Extraversion": 72,
            "Agreeableness": 84, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.20, "Extraversion": 0.25,
            "Agreeableness": 0.30, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "MBA HR / XLRI",
        "work_style": ["social", "communication", "structured"],
    },

    {
        "id": "supply_chain_manager",
        "name": "Supply Chain Manager",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Oversee procurement, logistics and distribution networks end-to-end.",
        "ocean_profile": {
            "Openness": 60, "Conscientiousness": 86, "Extraversion": 55,
            "Agreeableness": 58, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.40, "Extraversion": 0.20,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "MBA Operations",
        "work_style": ["structured", "strategic", "analytical"],
    },

    {
        "id": "stock_broker",
        "name": "Stock Broker / Equity Analyst",
        "category": "Business & Finance",
        "source": "indian",
        "description": "Analyse securities and execute trades on behalf of clients or institutions.",
        "ocean_profile": {
            "Openness": 65, "Conscientiousness": 78, "Extraversion": 68,
            "Agreeableness": 48, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.30, "Extraversion": 0.25,
            "Agreeableness": 0.10, "Neuroticism": 0.20,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "NISM / SEBI certification",
        "work_style": ["analytical", "strategic", "independent"],
    },

    {
        "id": "real_estate",
        "name": "Real Estate Developer / Agent",
        "category": "Business & Finance",
        "source": "hybrid",
        "description": "Buy, sell, develop and manage properties and land.",
        "ocean_profile": {
            "Openness": 62, "Conscientiousness": 72, "Extraversion": 78,
            "Agreeableness": 65, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.20, "Extraversion": 0.35,
            "Agreeableness": 0.20, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["social", "entrepreneurial", "strategic"],
    },

    # ── LAW & CIVIL SERVICES ─────────────────────────────────

    {
        "id": "ias_officer",
        "name": "IAS / Civil Services Officer",
        "category": "Law & Civil Services",
        "source": "indian",
        "description": "Administer public policy and governance at district and national level.",
        "ocean_profile": {
            "Openness": 74, "Conscientiousness": 84, "Extraversion": 65,
            "Agreeableness": 68, "Neuroticism": 20,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.30, "Extraversion": 0.20,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UPSC CSE",
        "work_style": ["leadership", "structured", "strategic"],
    },

    {
        "id": "lawyer",
        "name": "Lawyer / Advocate",
        "category": "Law & Civil Services",
        "source": "hybrid",
        "description": "Represent clients, argue cases and provide legal counsel.",
        "ocean_profile": {
            "Openness": 74, "Conscientiousness": 78, "Extraversion": 72,
            "Agreeableness": 54, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.25, "Extraversion": 0.30,
            "Agreeableness": 0.10, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "CLAT / AILET",
        "work_style": ["analytical", "communication", "strategic"],
    },

    {
        "id": "judge",
        "name": "Judge",
        "category": "Law & Civil Services",
        "source": "hybrid",
        "description": "Preside over court proceedings and deliver impartial legal judgements.",
        "ocean_profile": {
            "Openness": 68, "Conscientiousness": 90, "Extraversion": 48,
            "Agreeableness": 60, "Neuroticism": 20,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.40, "Extraversion": 0.10,
            "Agreeableness": 0.20, "Neuroticism": 0.15,
        },
        "user_types": ["professional"],
        "entrance_exam": "Judicial Services Exam / HJS",
        "work_style": ["analytical", "structured", "independent"],
    },

    {
        "id": "policy_analyst",
        "name": "Policy Analyst",
        "category": "Law & Civil Services",
        "source": "onet",
        "description": "Research and evaluate public policies to inform government decisions.",
        "ocean_profile": {
            "Openness": 80, "Conscientiousness": 76, "Extraversion": 55,
            "Agreeableness": 65, "Neuroticism": 26,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.25, "Extraversion": 0.15,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UPSC / State PSC",
        "work_style": ["analytical", "research", "strategic"],
    },

    {
        "id": "corporate_lawyer",
        "name": "Corporate Lawyer",
        "category": "Law & Civil Services",
        "source": "hybrid",
        "description": "Handle mergers, acquisitions, contracts and corporate compliance.",
        "ocean_profile": {
            "Openness": 68, "Conscientiousness": 86, "Extraversion": 60,
            "Agreeableness": 52, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.35, "Extraversion": 0.20,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "CLAT / LLB / LLM",
        "work_style": ["analytical", "strategic", "structured"],
    },

    {
        "id": "diplomat",
        "name": "Diplomat / Foreign Service Officer",
        "category": "Law & Civil Services",
        "source": "indian",
        "description": "Represent India's interests abroad and manage international relations.",
        "ocean_profile": {
            "Openness": 80, "Conscientiousness": 78, "Extraversion": 72,
            "Agreeableness": 72, "Neuroticism": 20,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.20, "Extraversion": 0.25,
            "Agreeableness": 0.25, "Neuroticism": 0.05,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UPSC IFS",
        "work_style": ["communication", "strategic", "social"],
    },

    # ── CREATIVE & MEDIA ─────────────────────────────────────

    {
        "id": "graphic_designer",
        "name": "Graphic Designer",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Create visual content for brands, media and digital platforms.",
        "ocean_profile": {
            "Openness": 88, "Conscientiousness": 58, "Extraversion": 50,
            "Agreeableness": 65, "Neuroticism": 36,
        },
        "weights": {
            "Openness": 0.40, "Conscientiousness": 0.15, "Extraversion": 0.15,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["class_10", "class_12", "undergraduate", "professional"],
        "entrance_exam": "NID / NIFT entrance",
        "work_style": ["creative", "artistic", "independent"],
    },

    {
        "id": "journalist",
        "name": "Journalist",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Investigate, report and communicate news and stories to the public.",
        "ocean_profile": {
            "Openness": 84, "Conscientiousness": 64, "Extraversion": 74,
            "Agreeableness": 60, "Neuroticism": 36,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.15, "Extraversion": 0.30,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "IIMC / ACJ / Mass comm",
        "work_style": ["communication", "research", "creative"],
    },

    {
        "id": "filmmaker",
        "name": "Filmmaker / Director",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Conceptualise and direct films, web series and video content.",
        "ocean_profile": {
            "Openness": 90, "Conscientiousness": 62, "Extraversion": 70,
            "Agreeableness": 60, "Neuroticism": 40,
        },
        "weights": {
            "Openness": 0.40, "Conscientiousness": 0.15, "Extraversion": 0.20,
            "Agreeableness": 0.10, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "FTII / SRFTI entrance",
        "work_style": ["creative", "artistic", "leadership"],
    },

    {
        "id": "content_writer",
        "name": "Content Writer / Author",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Create written content for digital, print and broadcast media.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 58, "Extraversion": 40,
            "Agreeableness": 62, "Neuroticism": 38,
        },
        "weights": {
            "Openness": 0.45, "Conscientiousness": 0.15, "Extraversion": 0.08,
            "Agreeableness": 0.15, "Neuroticism": 0.17,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["creative", "independent", "research"],
    },

    {
        "id": "architect",
        "name": "Architect",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Design buildings and spaces that are functional, safe and aesthetically compelling.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 78, "Extraversion": 52,
            "Agreeableness": 60, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.35, "Conscientiousness": 0.30, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NATA / JEE Paper 2",
        "work_style": ["creative", "technical", "artistic"],
    },

    {
        "id": "photographer",
        "name": "Photographer / Videographer",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Capture and edit visual stories through photography and video.",
        "ocean_profile": {
            "Openness": 88, "Conscientiousness": 55, "Extraversion": 54,
            "Agreeableness": 65, "Neuroticism": 36,
        },
        "weights": {
            "Openness": 0.45, "Conscientiousness": 0.15, "Extraversion": 0.15,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["class_10", "class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["creative", "artistic", "independent"],
    },

    {
        "id": "fashion_designer",
        "name": "Fashion Designer",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Design clothing, accessories and fashion collections.",
        "ocean_profile": {
            "Openness": 90, "Conscientiousness": 60, "Extraversion": 62,
            "Agreeableness": 60, "Neuroticism": 36,
        },
        "weights": {
            "Openness": 0.45, "Conscientiousness": 0.15, "Extraversion": 0.15,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["class_10", "class_12", "undergraduate"],
        "entrance_exam": "NIFT / NID entrance",
        "work_style": ["creative", "artistic", "entrepreneurial"],
    },

    {
        "id": "musician",
        "name": "Musician / Music Producer",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Compose, perform and produce music across genres and formats.",
        "ocean_profile": {
            "Openness": 90, "Conscientiousness": 55, "Extraversion": 65,
            "Agreeableness": 68, "Neuroticism": 42,
        },
        "weights": {
            "Openness": 0.45, "Conscientiousness": 0.10, "Extraversion": 0.20,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["class_10", "class_12", "undergraduate", "professional"],
        "entrance_exam": "Music college auditions",
        "work_style": ["creative", "artistic", "independent"],
    },

    {
        "id": "animator",
        "name": "Animator / Motion Designer",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Create animated visuals for films, games, advertising and digital media.",
        "ocean_profile": {
            "Openness": 88, "Conscientiousness": 66, "Extraversion": 44,
            "Agreeableness": 60, "Neuroticism": 34,
        },
        "weights": {
            "Openness": 0.40, "Conscientiousness": 0.25, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "Arena / MAAC / DSK",
        "work_style": ["creative", "technical", "artistic"],
    },

    {
        "id": "art_director",
        "name": "Art Director",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Lead the visual direction for advertising, publishing or media productions.",
        "ocean_profile": {
            "Openness": 88, "Conscientiousness": 66, "Extraversion": 62,
            "Agreeableness": 60, "Neuroticism": 34,
        },
        "weights": {
            "Openness": 0.35, "Conscientiousness": 0.20, "Extraversion": 0.20,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "NID / NIFT / Portfolio",
        "work_style": ["creative", "leadership", "strategic"],
    },

    {
        "id": "copywriter",
        "name": "Copywriter / Creative Director",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Write compelling copy for advertising, branding and marketing campaigns.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 60, "Extraversion": 60,
            "Agreeableness": 62, "Neuroticism": 36,
        },
        "weights": {
            "Openness": 0.40, "Conscientiousness": 0.15, "Extraversion": 0.20,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["creative", "strategic", "communication"],
    },

    # ── EDUCATION & SOCIAL IMPACT ────────────────────────────

    {
        "id": "school_teacher",
        "name": "School Teacher",
        "category": "Education & Social Impact",
        "source": "hybrid",
        "description": "Educate and mentor students at primary or secondary school level.",
        "ocean_profile": {
            "Openness": 66, "Conscientiousness": 72, "Extraversion": 68,
            "Agreeableness": 84, "Neuroticism": 32,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.20, "Extraversion": 0.25,
            "Agreeableness": 0.30, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "B.Ed / CTET / TET",
        "work_style": ["caregiving", "communication", "structured"],
    },

    {
        "id": "social_worker",
        "name": "Social Worker / NGO Professional",
        "category": "Education & Social Impact",
        "source": "onet",
        "description": "Support individuals and communities facing social, economic or health challenges.",
        "ocean_profile": {
            "Openness": 70, "Conscientiousness": 66, "Extraversion": 65,
            "Agreeableness": 88, "Neuroticism": 36,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.15, "Extraversion": 0.20,
            "Agreeableness": 0.40, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "MSW entrance",
        "work_style": ["caregiving", "collaborative", "social"],
    },

    {
        "id": "psychologist",
        "name": "Psychologist / Counsellor",
        "category": "Education & Social Impact",
        "source": "onet",
        "description": "Assess and support individuals with mental, emotional and behavioural challenges.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 70, "Extraversion": 58,
            "Agreeableness": 86, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.15, "Extraversion": 0.20,
            "Agreeableness": 0.30, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "MA Psychology / RCI",
        "work_style": ["caregiving", "analytical", "research"],
    },

    {
        "id": "career_counsellor",
        "name": "Career Counsellor",
        "category": "Education & Social Impact",
        "source": "hybrid",
        "description": "Guide students and professionals through career decisions and transitions.",
        "ocean_profile": {
            "Openness": 74, "Conscientiousness": 70, "Extraversion": 70,
            "Agreeableness": 86, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.15, "Extraversion": 0.25,
            "Agreeableness": 0.30, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "M.Ed / Counselling certification",
        "work_style": ["caregiving", "communication", "social"],
    },

    {
        "id": "special_educator",
        "name": "Special Educator",
        "category": "Education & Social Impact",
        "source": "onet",
        "description": "Teach and support students with learning disabilities and special needs.",
        "ocean_profile": {
            "Openness": 68, "Conscientiousness": 74, "Extraversion": 62,
            "Agreeableness": 90, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.20, "Extraversion": 0.15,
            "Agreeableness": 0.40, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "B.Ed Special Education / RCI",
        "work_style": ["caregiving", "structured", "hands_on"],
    },

    {
        "id": "development_sector",
        "name": "Development Sector Professional",
        "category": "Education & Social Impact",
        "source": "hybrid",
        "description": "Work on international development, poverty alleviation and social programmes.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 70, "Extraversion": 65,
            "Agreeableness": 84, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.20, "Extraversion": 0.20,
            "Agreeableness": 0.30, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "IRMA / Tata Institute / IIFM",
        "work_style": ["strategic", "collaborative", "social"],
    },

    # ── DEFENCE & GOVERNMENT ─────────────────────────────────

    {
        "id": "army_officer",
        "name": "Army Officer",
        "category": "Defence & Government",
        "source": "indian",
        "description": "Lead military operations and manage personnel in the Indian Army.",
        "ocean_profile": {
            "Openness": 52, "Conscientiousness": 88, "Extraversion": 70,
            "Agreeableness": 60, "Neuroticism": 20,
        },
        "weights": {
            "Openness": 0.08, "Conscientiousness": 0.40, "Extraversion": 0.25,
            "Agreeableness": 0.12, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NDA / CDS / AFCAT",
        "work_style": ["leadership", "structured", "hands_on"],
    },

    {
        "id": "police_officer",
        "name": "Police Officer / IPS",
        "category": "Defence & Government",
        "source": "indian",
        "description": "Enforce law, investigate crimes and maintain public order.",
        "ocean_profile": {
            "Openness": 55, "Conscientiousness": 84, "Extraversion": 65,
            "Agreeableness": 58, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.35, "Extraversion": 0.25,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UPSC CSE (IPS) / State PSC",
        "work_style": ["leadership", "structured", "problem_solving"],
    },

    {
        "id": "navy_officer",
        "name": "Navy Officer",
        "category": "Defence & Government",
        "source": "indian",
        "description": "Serve in the Indian Navy managing naval operations and personnel.",
        "ocean_profile": {
            "Openness": 56, "Conscientiousness": 86, "Extraversion": 64,
            "Agreeableness": 58, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.08, "Conscientiousness": 0.40, "Extraversion": 0.22,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NDA / CDSE / SSB",
        "work_style": ["leadership", "technical", "structured"],
    },

    {
        "id": "ifs_officer",
        "name": "Indian Forest Service (IFS) Officer",
        "category": "Defence & Government",
        "source": "indian",
        "description": "Manage and conserve India's forests, wildlife and natural resources.",
        "ocean_profile": {
            "Openness": 70, "Conscientiousness": 80, "Extraversion": 55,
            "Agreeableness": 70, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.30, "Extraversion": 0.15,
            "Agreeableness": 0.25, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UPSC IFS",
        "work_style": ["hands_on", "structured", "independent"],
    },

    {
        "id": "rbi_officer",
        "name": "RBI / Banking Officer (IBPS)",
        "category": "Defence & Government",
        "source": "indian",
        "description": "Manage monetary policy, banking operations or financial regulation.",
        "ocean_profile": {
            "Openness": 58, "Conscientiousness": 86, "Extraversion": 52,
            "Agreeableness": 58, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.45, "Extraversion": 0.15,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "RBI Grade B / IBPS PO",
        "work_style": ["structured", "analytical", "independent"],
    },

    # ── SCIENCE & ENVIRONMENT ────────────────────────────────

    {
        "id": "environmental_scientist",
        "name": "Environmental Scientist",
        "category": "Science & Environment",
        "source": "onet",
        "description": "Study the environment and develop solutions to ecological problems.",
        "ocean_profile": {
            "Openness": 80, "Conscientiousness": 74, "Extraversion": 48,
            "Agreeableness": 70, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.25, "Extraversion": 0.10,
            "Agreeableness": 0.25, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "GATE (Environmental) / IFS",
        "work_style": ["research", "hands_on", "analytical"],
    },

    {
        "id": "biotechnologist",
        "name": "Biotechnologist",
        "category": "Science & Environment",
        "source": "hybrid",
        "description": "Apply biology and technology to develop products in medicine, agriculture and industry.",
        "ocean_profile": {
            "Openness": 80, "Conscientiousness": 82, "Extraversion": 40,
            "Agreeableness": 55, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.35, "Extraversion": 0.08,
            "Agreeableness": 0.12, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NEET / JEE / GATE (BT)",
        "work_style": ["analytical", "research", "technical"],
    },

    {
        "id": "pharmacist",
        "name": "Pharmacist",
        "category": "Science & Environment",
        "source": "onet",
        "description": "Dispense medication and counsel patients on drug use and interactions.",
        "ocean_profile": {
            "Openness": 58, "Conscientiousness": 86, "Extraversion": 55,
            "Agreeableness": 74, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.40, "Extraversion": 0.15,
            "Agreeableness": 0.25, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NEET / B.Pharm entrance",
        "work_style": ["structured", "caregiving", "technical"],
    },

    {
        "id": "geologist",
        "name": "Geologist",
        "category": "Science & Environment",
        "source": "onet",
        "description": "Study the Earth's structure, composition and geological processes.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 76, "Extraversion": 40,
            "Agreeableness": 55, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.30, "Extraversion": 0.08,
            "Agreeableness": 0.17, "Neuroticism": 0.15,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "GATE (GG) / GSI recruitment",
        "work_style": ["research", "hands_on", "analytical"],
    },

    {
        "id": "astrophysicist",
        "name": "Astrophysicist / Astronomer",
        "category": "Science & Environment",
        "source": "onet",
        "description": "Study celestial objects, space and the physical universe.",
        "ocean_profile": {
            "Openness": 90, "Conscientiousness": 78, "Extraversion": 30,
            "Agreeableness": 52, "Neuroticism": 22,
        },
        "weights": {
            "Openness": 0.40, "Conscientiousness": 0.30, "Extraversion": 0.05,
            "Agreeableness": 0.12, "Neuroticism": 0.13,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEST / ISRO / IIA recruitment",
        "work_style": ["research", "analytical", "independent"],
    },

    {
        "id": "marine_biologist",
        "name": "Marine Biologist",
        "category": "Science & Environment",
        "source": "onet",
        "description": "Study ocean ecosystems, marine organisms and underwater environments.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 70, "Extraversion": 48,
            "Agreeableness": 68, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.35, "Conscientiousness": 0.25, "Extraversion": 0.10,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "CSIR-NET / ICAR / NIO",
        "work_style": ["research", "hands_on", "independent"],
    },

    {
        "id": "agricultural_scientist",
        "name": "Agricultural Scientist",
        "category": "Science & Environment",
        "source": "indian",
        "description": "Research and improve crop production, soil health and farming practices.",
        "ocean_profile": {
            "Openness": 70, "Conscientiousness": 76, "Extraversion": 50,
            "Agreeableness": 68, "Neuroticism": 26,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.30, "Extraversion": 0.10,
            "Agreeableness": 0.25, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "ICAR AIEEA / PAU / IARI",
        "work_style": ["hands_on", "research", "structured"],
    },

    # ── HOSPITALITY, SPORTS & WELLNESS ──────────────────────

    {
        "id": "hotel_manager",
        "name": "Hotel / Hospitality Manager",
        "category": "Hospitality & Sports",
        "source": "onet",
        "description": "Oversee hotel operations and ensure exceptional guest experiences.",
        "ocean_profile": {
            "Openness": 62, "Conscientiousness": 76, "Extraversion": 80,
            "Agreeableness": 78, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.20, "Extraversion": 0.35,
            "Agreeableness": 0.25, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "IHM entrance / NCHMCT JEE",
        "work_style": ["social", "leadership", "structured"],
    },

    {
        "id": "sports_coach",
        "name": "Sports Coach / Athlete",
        "category": "Hospitality & Sports",
        "source": "onet",
        "description": "Train athletes and develop sports programmes at competitive levels.",
        "ocean_profile": {
            "Openness": 60, "Conscientiousness": 78, "Extraversion": 75,
            "Agreeableness": 68, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.30, "Extraversion": 0.30,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["class_10", "class_12", "undergraduate"],
        "entrance_exam": "NIS Patiala / SAI",
        "work_style": ["leadership", "hands_on", "social"],
    },

    {
        "id": "yoga_instructor",
        "name": "Yoga Instructor / Wellness Coach",
        "category": "Hospitality & Sports",
        "source": "hybrid",
        "description": "Guide individuals through physical and mental wellness practices.",
        "ocean_profile": {
            "Openness": 70, "Conscientiousness": 64, "Extraversion": 62,
            "Agreeableness": 84, "Neuroticism": 24,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.15, "Extraversion": 0.20,
            "Agreeableness": 0.35, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "Yoga certification / AYUSH",
        "work_style": ["caregiving", "independent", "hands_on"],
    },

    {
        "id": "event_manager",
        "name": "Event Manager",
        "category": "Hospitality & Sports",
        "source": "onet",
        "description": "Plan, coordinate and execute large-scale events, conferences and productions.",
        "ocean_profile": {
            "Openness": 70, "Conscientiousness": 78, "Extraversion": 82,
            "Agreeableness": 68, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.15, "Conscientiousness": 0.25, "Extraversion": 0.30,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["social", "structured", "leadership"],
    },

    {
        "id": "travel_consultant",
        "name": "Travel Consultant / Tour Operator",
        "category": "Hospitality & Sports",
        "source": "onet",
        "description": "Plan and sell travel experiences for individuals and groups.",
        "ocean_profile": {
            "Openness": 76, "Conscientiousness": 68, "Extraversion": 78,
            "Agreeableness": 72, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.20, "Conscientiousness": 0.15, "Extraversion": 0.35,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["social", "creative", "entrepreneurial"],
    },

    # ── STREAM GUIDANCE (Class 10) ───────────────────────────

    {
        "id": "stream_science",
        "name": "Science Stream (PCM / PCB)",
        "category": "Stream Selection",
        "source": "indian",
        "description": "Foundation for engineering, medicine, research and technology careers.",
        "ocean_profile": {
            "Openness": 70, "Conscientiousness": 78, "Extraversion": 42,
            "Agreeableness": 52, "Neuroticism": 26,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.35, "Extraversion": 0.10,
            "Agreeableness": 0.15, "Neuroticism": 0.15,
        },
        "user_types": ["class_10"],
        "entrance_exam": "JEE / NEET (after 12th)",
        "work_style": ["analytical", "structured", "research"],
    },

    {
        "id": "stream_commerce",
        "name": "Commerce Stream",
        "category": "Stream Selection",
        "source": "indian",
        "description": "Foundation for finance, business, law and economics careers.",
        "ocean_profile": {
            "Openness": 55, "Conscientiousness": 78, "Extraversion": 58,
            "Agreeableness": 60, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.10, "Conscientiousness": 0.35, "Extraversion": 0.25,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["class_10"],
        "entrance_exam": "CA Foundation / CLAT / CAT (after degree)",
        "work_style": ["structured", "social", "analytical"],
    },

    {
        "id": "stream_arts",
        "name": "Arts / Humanities Stream",
        "category": "Stream Selection",
        "source": "indian",
        "description": "Foundation for social sciences, law, journalism, design and creative careers.",
        "ocean_profile": {
            "Openness": 86, "Conscientiousness": 58, "Extraversion": 62,
            "Agreeableness": 74, "Neuroticism": 36,
        },
        "weights": {
            "Openness": 0.40, "Conscientiousness": 0.10, "Extraversion": 0.20,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["class_10"],
        "entrance_exam": "CLAT / UPSC / Mass comm (after 12th)",
        "work_style": ["creative", "communication", "social"],
    },

    # ── EMERGING & FREELANCE ─────────────────────────────────

    {
        "id": "social_media_manager",
        "name": "Social Media Manager",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Build and manage brand presence across social media platforms.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 64, "Extraversion": 80,
            "Agreeableness": 68, "Neuroticism": 32,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.15, "Extraversion": 0.35,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["creative", "social", "strategic"],
    },

    {
        "id": "edtech_professional",
        "name": "EdTech Professional",
        "category": "Education & Social Impact",
        "source": "hybrid",
        "description": "Build and deliver digital learning products and educational technology solutions.",
        "ocean_profile": {
            "Openness": 78, "Conscientiousness": 70, "Extraversion": 62,
            "Agreeableness": 72, "Neuroticism": 28,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.25, "Extraversion": 0.20,
            "Agreeableness": 0.20, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["technical", "collaborative", "creative"],
    },

    {
        "id": "startup_founder",
        "name": "Startup Founder / Co-founder",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Ideate, build and grow a startup from zero to scale.",
        "ocean_profile": {
            "Openness": 88, "Conscientiousness": 72, "Extraversion": 80,
            "Agreeableness": 58, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.20, "Extraversion": 0.25,
            "Agreeableness": 0.10, "Neuroticism": 0.15,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["entrepreneurial", "leadership", "strategic"],
    },

    {
        "id": "ngo_founder",
        "name": "NGO Founder / Social Entrepreneur",
        "category": "Education & Social Impact",
        "source": "hybrid",
        "description": "Build organisations that address social, environmental and community problems.",
        "ocean_profile": {
            "Openness": 84, "Conscientiousness": 68, "Extraversion": 72,
            "Agreeableness": 86, "Neuroticism": 30,
        },
        "weights": {
            "Openness": 0.25, "Conscientiousness": 0.15, "Extraversion": 0.20,
            "Agreeableness": 0.30, "Neuroticism": 0.10,
        },
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["collaborative", "leadership", "social"],
    },

    {
        "id": "content_creator",
        "name": "Content Creator / Influencer",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Build and monetise an audience through video, blogs or social media content.",
        "ocean_profile": {
            "Openness": 84, "Conscientiousness": 55, "Extraversion": 82,
            "Agreeableness": 65, "Neuroticism": 36,
        },
        "weights": {
            "Openness": 0.30, "Conscientiousness": 0.10, "Extraversion": 0.35,
            "Agreeableness": 0.15, "Neuroticism": 0.10,
        },
        "user_types": ["class_10", "class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["creative", "entrepreneurial", "social"],
    },
]


# ── VALIDATION ───────────────────────────────────────────────

REQUIRED_CAREER_FIELDS = {
    "id", "name", "category", "source",
    "description", "ocean_profile", "weights", "work_style",
}


def validate_profiles() -> None:
    """
    Validate all career profiles for schema correctness, value ranges,
    weight sums, standardized tags, and ID uniqueness.
    Raises ValueError with a descriptive message on the first failure found.
    """
    seen_ids: set = set()

    for career in CAREERS:
        cid = career.get("id", "<missing id>")
        name = career.get("name", cid)

        # 1. Required fields
        missing = REQUIRED_CAREER_FIELDS - career.keys()
        if missing:
            raise ValueError(
                f"[{cid}] Missing required fields: {missing}"
            )

        # 2. Unique IDs
        if cid in seen_ids:
            raise ValueError(f"Duplicate career id: '{cid}'")
        seen_ids.add(cid)

        # 3. Valid source
        if career["source"] not in VALID_SOURCES:
            raise ValueError(
                f"[{cid}] Invalid source '{career['source']}'. "
                f"Must be one of {VALID_SOURCES}."
            )

        ocean = career["ocean_profile"]
        weights = career["weights"]

        # 4. All OCEAN traits present
        for field_name, mapping in (("ocean_profile", ocean), ("weights", weights)):
            missing_traits = set(REQUIRED_TRAITS) - mapping.keys()
            if missing_traits:
                raise ValueError(
                    f"[{cid}] '{field_name}' is missing traits: {missing_traits}"
                )

        # 5. OCEAN value ranges (20–90)
        for trait in REQUIRED_TRAITS:
            val = ocean[trait]
            if not isinstance(val, (int, float)):
                raise ValueError(
                    f"[{cid}] ocean_profile['{trait}'] must be numeric, got {type(val).__name__}"
                )
            if not (20 <= val <= 90):
                raise ValueError(
                    f"[{cid}] ocean_profile['{trait}'] = {val} is out of range [20, 90]"
                )

        # 6. Weight ranges and sum
        for trait in REQUIRED_TRAITS:
            w = weights[trait]
            if not isinstance(w, (int, float)):
                raise ValueError(
                    f"[{cid}] weights['{trait}'] must be numeric, got {type(w).__name__}"
                )
            if not (0.0 <= w <= 1.0):
                raise ValueError(
                    f"[{cid}] weights['{trait}'] = {w} is out of range [0, 1]"
                )

        weight_sum = sum(weights[t] for t in REQUIRED_TRAITS)
        if abs(weight_sum - 1.0) > 0.01:
            raise ValueError(
                f"[{cid}] weights sum to {weight_sum:.4f}, expected 1.0 (±0.01)"
            )

        # 7. Standardized work_style tags
        styles = career["work_style"]
        if not isinstance(styles, list) or len(styles) == 0:
            raise ValueError(f"[{cid}] 'work_style' must be a non-empty list")

        invalid_styles = set(styles) - STANDARD_WORK_STYLES
        if invalid_styles:
            raise ValueError(
                f"[{cid}] Non-standard work_style tags: {invalid_styles}. "
                f"Allowed: {STANDARD_WORK_STYLES}"
            )


# Run validation automatically at import time
validate_profiles()


# ── LOOKUPS ──────────────────────────────────────────────────

CAREER_LOOKUP = {c["id"]: c for c in CAREERS}
CATEGORIES = sorted(set(c["category"] for c in CAREERS))