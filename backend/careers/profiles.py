# ============================================================
# EDWISERR — Career Profiles Dataset
# Hybrid: O*NET-derived (global) + Indian careers layer
#
# Each career has:
#   ocean_profile : ideal OCEAN trait scores (0–100)
#   category      : career cluster
#   source        : 'onet' | 'indian' | 'hybrid'
#   user_types    : which user types can be shown this career
#   entrance_exam : Indian entrance exam (if applicable)
#   description   : one-line summary
#
# OCEAN trait direction (all 5 traits, higher = more of the trait):
#   Openness          : curiosity, creativity, abstract thinking
#   Conscientiousness : discipline, organisation, goal-orientation
#   Extraversion      : social energy, assertiveness, leadership
#   Agreeableness     : empathy, cooperation, people-focus
#   Neuroticism       : emotional sensitivity (lower = more stable)
# ============================================================

CAREERS = [

    # ── TECHNOLOGY & DATA ────────────────────────────────────

    {
        "id": "data_scientist",
        "name": "Data Scientist",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Analyse complex datasets to extract insights and build predictive models.",
        "ocean_profile": {"Openness": 82, "Conscientiousness": 80, "Extraversion": 38, "Agreeableness": 52, "Neuroticism": 22},
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
        "ocean_profile": {"Openness": 72, "Conscientiousness": 82, "Extraversion": 38, "Agreeableness": 50, "Neuroticism": 25},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "JEE (for CS degree pathway)",
        "work_style": ["technical", "systematic", "independent"],
    },
    {
        "id": "ml_engineer",
        "name": "Machine Learning Engineer",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Build and deploy ML models and AI systems at scale.",
        "ocean_profile": {"Openness": 85, "Conscientiousness": 82, "Extraversion": 35, "Agreeableness": 48, "Neuroticism": 20},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["analytical", "technical", "innovative"],
    },
    {
        "id": "cybersecurity_analyst",
        "name": "Cybersecurity Analyst",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Protect systems and networks from digital threats and attacks.",
        "ocean_profile": {"Openness": 70, "Conscientiousness": 88, "Extraversion": 35, "Agreeableness": 45, "Neuroticism": 20},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["detail-oriented", "vigilant", "independent"],
    },
    {
        "id": "ux_designer",
        "name": "UX/UI Designer",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Design intuitive, user-centred digital interfaces and experiences.",
        "ocean_profile": {"Openness": 88, "Conscientiousness": 65, "Extraversion": 58, "Agreeableness": 72, "Neuroticism": 35},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["creative", "empathetic", "collaborative"],
    },
    {
        "id": "product_manager",
        "name": "Product Manager",
        "category": "Technology & Data",
        "source": "onet",
        "description": "Lead product vision, strategy and cross-functional execution.",
        "ocean_profile": {"Openness": 78, "Conscientiousness": 78, "Extraversion": 70, "Agreeableness": 65, "Neuroticism": 28},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["strategic", "communicative", "leadership"],
    },

    # ── RESEARCH & ACADEMIA ──────────────────────────────────

    {
        "id": "research_scientist",
        "name": "Research Scientist",
        "category": "Research & Academia",
        "source": "onet",
        "description": "Conduct original research to advance knowledge in a scientific field.",
        "ocean_profile": {"Openness": 90, "Conscientiousness": 80, "Extraversion": 32, "Agreeableness": 52, "Neuroticism": 22},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "GATE / CSIR-NET / JEST",
        "work_style": ["analytical", "curious", "independent"],
    },
    {
        "id": "university_professor",
        "name": "University Professor",
        "category": "Research & Academia",
        "source": "hybrid",
        "description": "Teach, mentor students and conduct research at a university.",
        "ocean_profile": {"Openness": 88, "Conscientiousness": 75, "Extraversion": 60, "Agreeableness": 68, "Neuroticism": 25},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UGC-NET / PhD",
        "work_style": ["intellectual", "communicative", "mentoring"],
    },
    {
        "id": "data_analyst",
        "name": "Data Analyst",
        "category": "Research & Academia",
        "source": "onet",
        "description": "Interpret data and generate actionable business insights.",
        "ocean_profile": {"Openness": 72, "Conscientiousness": 82, "Extraversion": 42, "Agreeableness": 55, "Neuroticism": 25},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["analytical", "detail-oriented", "systematic"],
    },

    # ── MEDICINE & HEALTH ────────────────────────────────────

    {
        "id": "doctor_mbbs",
        "name": "Medical Doctor (MBBS)",
        "category": "Medicine & Health",
        "source": "indian",
        "description": "Diagnose and treat patients across clinical settings.",
        "ocean_profile": {"Openness": 65, "Conscientiousness": 90, "Extraversion": 58, "Agreeableness": 80, "Neuroticism": 18},
        "user_types": ["class_10", "class_12"],
        "entrance_exam": "NEET-UG",
        "work_style": ["caring", "disciplined", "high-stakes"],
    },
    {
        "id": "surgeon",
        "name": "Surgeon",
        "category": "Medicine & Health",
        "source": "onet",
        "description": "Perform surgical procedures to treat disease, injury and deformity.",
        "ocean_profile": {"Openness": 62, "Conscientiousness": 95, "Extraversion": 50, "Agreeableness": 58, "Neuroticism": 12},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "NEET-PG / MS",
        "work_style": ["precise", "calm-under-pressure", "technical"],
    },
    {
        "id": "psychiatrist",
        "name": "Psychiatrist",
        "category": "Medicine & Health",
        "source": "onet",
        "description": "Diagnose and treat mental health disorders using therapy and medication.",
        "ocean_profile": {"Openness": 80, "Conscientiousness": 78, "Extraversion": 55, "Agreeableness": 85, "Neuroticism": 28},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "NEET-PG / MD Psychiatry",
        "work_style": ["empathetic", "analytical", "patient"],
    },
    {
        "id": "physiotherapist",
        "name": "Physiotherapist",
        "category": "Medicine & Health",
        "source": "hybrid",
        "description": "Rehabilitate patients with physical impairments through exercise and therapy.",
        "ocean_profile": {"Openness": 62, "Conscientiousness": 78, "Extraversion": 62, "Agreeableness": 85, "Neuroticism": 28},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NEET / BPT entrance",
        "work_style": ["hands-on", "caring", "motivating"],
    },
    {
        "id": "public_health_specialist",
        "name": "Public Health Specialist",
        "category": "Medicine & Health",
        "source": "hybrid",
        "description": "Design and implement health programmes at community or national scale.",
        "ocean_profile": {"Openness": 75, "Conscientiousness": 75, "Extraversion": 65, "Agreeableness": 82, "Neuroticism": 28},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "MPH entrance / UPSC (IAS for health policy)",
        "work_style": ["strategic", "collaborative", "mission-driven"],
    },

    # ── ENGINEERING ──────────────────────────────────────────

    {
        "id": "civil_engineer",
        "name": "Civil Engineer",
        "category": "Engineering",
        "source": "hybrid",
        "description": "Design and oversee construction of infrastructure — roads, bridges, buildings.",
        "ocean_profile": {"Openness": 60, "Conscientiousness": 85, "Extraversion": 50, "Agreeableness": 58, "Neuroticism": 22},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE Main / JEE Advanced",
        "work_style": ["systematic", "practical", "leadership"],
    },
    {
        "id": "mechanical_engineer",
        "name": "Mechanical Engineer",
        "category": "Engineering",
        "source": "hybrid",
        "description": "Design and analyse mechanical systems, machines and thermal devices.",
        "ocean_profile": {"Openness": 65, "Conscientiousness": 85, "Extraversion": 45, "Agreeableness": 52, "Neuroticism": 22},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE Main / JEE Advanced",
        "work_style": ["technical", "systematic", "problem-solving"],
    },
    {
        "id": "electrical_engineer",
        "name": "Electrical Engineer",
        "category": "Engineering",
        "source": "hybrid",
        "description": "Design and develop electrical systems, circuits and power infrastructure.",
        "ocean_profile": {"Openness": 68, "Conscientiousness": 85, "Extraversion": 42, "Agreeableness": 50, "Neuroticism": 22},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE Main / JEE Advanced / GATE",
        "work_style": ["analytical", "precise", "technical"],
    },
    {
        "id": "aerospace_engineer",
        "name": "Aerospace Engineer",
        "category": "Engineering",
        "source": "onet",
        "description": "Design aircraft, spacecraft and related systems.",
        "ocean_profile": {"Openness": 80, "Conscientiousness": 88, "Extraversion": 40, "Agreeableness": 50, "Neuroticism": 18},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "JEE Advanced / IIST entrance",
        "work_style": ["innovative", "precise", "technical"],
    },

    # ── BUSINESS & FINANCE ───────────────────────────────────

    {
        "id": "chartered_accountant",
        "name": "Chartered Accountant (CA)",
        "category": "Business & Finance",
        "source": "indian",
        "description": "Manage financial reporting, auditing and taxation for organisations.",
        "ocean_profile": {"Openness": 50, "Conscientiousness": 92, "Extraversion": 45, "Agreeableness": 55, "Neuroticism": 22},
        "user_types": ["class_10", "class_12", "undergraduate"],
        "entrance_exam": "CA Foundation / ICAI",
        "work_style": ["detail-oriented", "rule-based", "precise"],
    },
    {
        "id": "investment_banker",
        "name": "Investment Banker",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Raise capital, execute M&A deals and advise corporations on financial strategy.",
        "ocean_profile": {"Openness": 68, "Conscientiousness": 88, "Extraversion": 72, "Agreeableness": 48, "Neuroticism": 22},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "CAT / CFA / MBA",
        "work_style": ["high-pressure", "analytical", "competitive"],
    },
    {
        "id": "financial_analyst",
        "name": "Financial Analyst",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Evaluate financial data to support investment and business decisions.",
        "ocean_profile": {"Openness": 65, "Conscientiousness": 85, "Extraversion": 48, "Agreeableness": 52, "Neuroticism": 25},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "CFA / MBA Finance",
        "work_style": ["analytical", "systematic", "research-driven"],
    },
    {
        "id": "entrepreneur",
        "name": "Entrepreneur",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Build and scale a business from idea to execution.",
        "ocean_profile": {"Openness": 88, "Conscientiousness": 72, "Extraversion": 78, "Agreeableness": 58, "Neuroticism": 28},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["risk-tolerant", "innovative", "leadership"],
    },
    {
        "id": "management_consultant",
        "name": "Management Consultant",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Solve complex business problems and advise organisations on strategy.",
        "ocean_profile": {"Openness": 78, "Conscientiousness": 82, "Extraversion": 72, "Agreeableness": 60, "Neuroticism": 22},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "CAT / GMAT / MBA",
        "work_style": ["analytical", "communicative", "structured"],
    },
    {
        "id": "actuary",
        "name": "Actuary",
        "category": "Business & Finance",
        "source": "onet",
        "description": "Use mathematics and statistics to assess financial risk.",
        "ocean_profile": {"Openness": 68, "Conscientiousness": 90, "Extraversion": 38, "Agreeableness": 50, "Neuroticism": 18},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "IAI / IFoA actuarial exams",
        "work_style": ["quantitative", "precise", "independent"],
    },

    # ── LAW & CIVIL SERVICES ─────────────────────────────────

    {
        "id": "ias_officer",
        "name": "IAS / Civil Services Officer",
        "category": "Law & Civil Services",
        "source": "indian",
        "description": "Administer public policy and governance at district and national level.",
        "ocean_profile": {"Openness": 75, "Conscientiousness": 85, "Extraversion": 65, "Agreeableness": 68, "Neuroticism": 18},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UPSC CSE",
        "work_style": ["leadership", "disciplined", "mission-driven"],
    },
    {
        "id": "lawyer",
        "name": "Lawyer / Advocate",
        "category": "Law & Civil Services",
        "source": "hybrid",
        "description": "Represent clients, argue cases and provide legal counsel.",
        "ocean_profile": {"Openness": 75, "Conscientiousness": 80, "Extraversion": 72, "Agreeableness": 55, "Neuroticism": 28},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "CLAT / AILET / Bar Council",
        "work_style": ["argumentative", "analytical", "communicative"],
    },
    {
        "id": "judge",
        "name": "Judge",
        "category": "Law & Civil Services",
        "source": "hybrid",
        "description": "Preside over court proceedings and deliver impartial legal judgements.",
        "ocean_profile": {"Openness": 70, "Conscientiousness": 92, "Extraversion": 50, "Agreeableness": 60, "Neuroticism": 12},
        "user_types": ["professional"],
        "entrance_exam": "Judicial Services Exam / HJS",
        "work_style": ["impartial", "analytical", "calm"],
    },
    {
        "id": "policy_analyst",
        "name": "Policy Analyst",
        "category": "Law & Civil Services",
        "source": "onet",
        "description": "Research and evaluate public policies to inform government decisions.",
        "ocean_profile": {"Openness": 82, "Conscientiousness": 78, "Extraversion": 55, "Agreeableness": 65, "Neuroticism": 25},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UPSC / State PSC",
        "work_style": ["analytical", "research-driven", "mission-driven"],
    },

    # ── CREATIVE & MEDIA ─────────────────────────────────────

    {
        "id": "graphic_designer",
        "name": "Graphic Designer",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Create visual content for brands, media and digital platforms.",
        "ocean_profile": {"Openness": 92, "Conscientiousness": 60, "Extraversion": 50, "Agreeableness": 65, "Neuroticism": 38},
        "user_types": ["class_10", "class_12", "undergraduate", "professional"],
        "entrance_exam": "NID / NIFT entrance",
        "work_style": ["creative", "visual", "independent"],
    },
    {
        "id": "journalist",
        "name": "Journalist",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Investigate, report and communicate news and stories to the public.",
        "ocean_profile": {"Openness": 85, "Conscientiousness": 65, "Extraversion": 75, "Agreeableness": 60, "Neuroticism": 38},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "IIMC / ACJ / Mass comm entrance",
        "work_style": ["curious", "communicative", "fast-paced"],
    },
    {
        "id": "filmmaker",
        "name": "Filmmaker / Director",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Conceptualise and direct films, web series and video content.",
        "ocean_profile": {"Openness": 95, "Conscientiousness": 65, "Extraversion": 70, "Agreeableness": 60, "Neuroticism": 42},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "FTII / SRFTI entrance",
        "work_style": ["creative", "visionary", "collaborative"],
    },
    {
        "id": "content_writer",
        "name": "Content Writer / Author",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Create written content for digital, print and broadcast media.",
        "ocean_profile": {"Openness": 88, "Conscientiousness": 60, "Extraversion": 42, "Agreeableness": 62, "Neuroticism": 40},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": None,
        "work_style": ["creative", "independent", "reflective"],
    },
    {
        "id": "architect",
        "name": "Architect",
        "category": "Creative & Media",
        "source": "onet",
        "description": "Design buildings and spaces that are functional, safe and aesthetically compelling.",
        "ocean_profile": {"Openness": 88, "Conscientiousness": 80, "Extraversion": 52, "Agreeableness": 60, "Neuroticism": 30},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NATA / JEE Paper 2",
        "work_style": ["creative", "technical", "detail-oriented"],
    },

    # ── EDUCATION & SOCIAL IMPACT ────────────────────────────

    {
        "id": "school_teacher",
        "name": "School Teacher",
        "category": "Education & Social Impact",
        "source": "hybrid",
        "description": "Educate and mentor students at primary or secondary school level.",
        "ocean_profile": {"Openness": 68, "Conscientiousness": 72, "Extraversion": 68, "Agreeableness": 85, "Neuroticism": 32},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "B.Ed / CTET / TET",
        "work_style": ["nurturing", "patient", "communicative"],
    },
    {
        "id": "social_worker",
        "name": "Social Worker / NGO Professional",
        "category": "Education & Social Impact",
        "source": "onet",
        "description": "Support individuals and communities facing social, economic or health challenges.",
        "ocean_profile": {"Openness": 72, "Conscientiousness": 68, "Extraversion": 65, "Agreeableness": 90, "Neuroticism": 38},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "MSW entrance",
        "work_style": ["empathetic", "mission-driven", "collaborative"],
    },
    {
        "id": "psychologist",
        "name": "Psychologist / Counsellor",
        "category": "Education & Social Impact",
        "source": "onet",
        "description": "Assess and support individuals with mental, emotional and behavioural challenges.",
        "ocean_profile": {"Openness": 80, "Conscientiousness": 72, "Extraversion": 58, "Agreeableness": 88, "Neuroticism": 30},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "MA Psychology / RCI for rehab",
        "work_style": ["empathetic", "analytical", "patient"],
    },

    # ── DEFENCE & GOVERNMENT ─────────────────────────────────

    {
        "id": "army_officer",
        "name": "Army Officer",
        "category": "Defence & Government",
        "source": "indian",
        "description": "Lead military operations and manage personnel in the Indian Army.",
        "ocean_profile": {"Openness": 55, "Conscientiousness": 90, "Extraversion": 70, "Agreeableness": 60, "Neuroticism": 10},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NDA / CDS / AFCAT",
        "work_style": ["leadership", "disciplined", "high-stakes"],
    },
    {
        "id": "police_officer",
        "name": "Police Officer / IPS",
        "category": "Defence & Government",
        "source": "indian",
        "description": "Enforce law, investigate crimes and maintain public order.",
        "ocean_profile": {"Openness": 58, "Conscientiousness": 85, "Extraversion": 65, "Agreeableness": 58, "Neuroticism": 15},
        "user_types": ["undergraduate", "professional"],
        "entrance_exam": "UPSC CSE (IPS) / State PSC",
        "work_style": ["assertive", "disciplined", "adaptive"],
    },

    # ── SCIENCE & ENVIRONMENT ────────────────────────────────

    {
        "id": "environmental_scientist",
        "name": "Environmental Scientist",
        "category": "Science & Environment",
        "source": "onet",
        "description": "Study the environment and develop solutions to ecological problems.",
        "ocean_profile": {"Openness": 82, "Conscientiousness": 75, "Extraversion": 48, "Agreeableness": 70, "Neuroticism": 28},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "GATE (Environmental) / IFS",
        "work_style": ["curious", "mission-driven", "field-based"],
    },
    {
        "id": "biotechnologist",
        "name": "Biotechnologist",
        "category": "Science & Environment",
        "source": "hybrid",
        "description": "Apply biology and technology to develop products in medicine, agriculture and industry.",
        "ocean_profile": {"Openness": 82, "Conscientiousness": 82, "Extraversion": 40, "Agreeableness": 55, "Neuroticism": 22},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NEET / JEE / GATE (BT)",
        "work_style": ["analytical", "curious", "lab-based"],
    },
    {
        "id": "pharmacist",
        "name": "Pharmacist",
        "category": "Science & Environment",
        "source": "onet",
        "description": "Dispense medication and counsel patients on drug use and interactions.",
        "ocean_profile": {"Openness": 60, "Conscientiousness": 88, "Extraversion": 55, "Agreeableness": 75, "Neuroticism": 22},
        "user_types": ["class_12", "undergraduate"],
        "entrance_exam": "NEET / B.Pharm entrance",
        "work_style": ["precise", "caring", "systematic"],
    },

    # ── HOSPITALITY & SPORTS ─────────────────────────────────

    {
        "id": "hotel_manager",
        "name": "Hotel / Hospitality Manager",
        "category": "Hospitality & Tourism",
        "source": "onet",
        "description": "Oversee hotel operations and ensure exceptional guest experiences.",
        "ocean_profile": {"Openness": 65, "Conscientiousness": 78, "Extraversion": 80, "Agreeableness": 80, "Neuroticism": 28},
        "user_types": ["class_12", "undergraduate", "professional"],
        "entrance_exam": "IHM entrance / NCHMCT JEE",
        "work_style": ["service-oriented", "leadership", "social"],
    },
    {
        "id": "sports_coach",
        "name": "Sports Coach / Athlete",
        "category": "Hospitality & Sports",
        "source": "onet",
        "description": "Train athletes and develop sports programmes at competitive levels.",
        "ocean_profile": {"Openness": 62, "Conscientiousness": 80, "Extraversion": 75, "Agreeableness": 68, "Neuroticism": 22},
        "user_types": ["class_10", "class_12", "undergraduate"],
        "entrance_exam": "NIS Patiala / Sports Authority of India",
        "work_style": ["motivating", "disciplined", "energetic"],
    },

    # ── STREAM GUIDANCE (Class 10) ───────────────────────────

    {
        "id": "stream_science",
        "name": "Science Stream (PCM / PCB)",
        "category": "Stream Selection",
        "source": "indian",
        "description": "Foundation for engineering, medicine, research and technology careers.",
        "ocean_profile": {"Openness": 72, "Conscientiousness": 80, "Extraversion": 42, "Agreeableness": 52, "Neuroticism": 25},
        "user_types": ["class_10"],
        "entrance_exam": "JEE / NEET (after 12th)",
        "work_style": ["analytical", "systematic", "curious"],
    },
    {
        "id": "stream_commerce",
        "name": "Commerce Stream",
        "category": "Stream Selection",
        "source": "indian",
        "description": "Foundation for finance, business, law and economics careers.",
        "ocean_profile": {"Openness": 58, "Conscientiousness": 80, "Extraversion": 58, "Agreeableness": 60, "Neuroticism": 28},
        "user_types": ["class_10"],
        "entrance_exam": "CA Foundation / CLAT / CAT (after degree)",
        "work_style": ["structured", "social", "goal-oriented"],
    },
    {
        "id": "stream_arts",
        "name": "Arts / Humanities Stream",
        "category": "Stream Selection",
        "source": "indian",
        "description": "Foundation for social sciences, law, journalism, design and creative careers.",
        "ocean_profile": {"Openness": 88, "Conscientiousness": 60, "Extraversion": 62, "Agreeableness": 75, "Neuroticism": 38},
        "user_types": ["class_10"],
        "entrance_exam": "CLAT / UPSC / Mass comm (after 12th)",
        "work_style": ["creative", "communicative", "empathetic"],
    },
]

# ── Career lookup by id ──────────────────────────────────────
CAREER_LOOKUP = {c['id']: c for c in CAREERS}

# ── Category registry ────────────────────────────────────────
CATEGORIES = sorted(set(c['category'] for c in CAREERS))

# ── Source tags ──────────────────────────────────────────────
# 'onet'   → validated against O*NET work style profiles
# 'indian' → India-specific careers (entrance exams, local context)
# 'hybrid' → O*NET base + Indian context layered