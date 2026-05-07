# ============================================================
# EDWISERR — Career Profiles Dataset (Expanded)
# 100+ careers: O*NET (global) + Indian careers layer
# ============================================================

CAREERS = [

    # ── TECHNOLOGY & DATA ────────────────────────────────────

    {"id":"data_scientist","name":"Data Scientist","category":"Technology & Data","source":"onet",
     "description":"Analyse complex datasets to extract insights and build predictive models.",
     "ocean_profile":{"Openness":82,"Conscientiousness":80,"Extraversion":38,"Agreeableness":52,"Neuroticism":22},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["analytical","independent","technical"]},

    {"id":"software_engineer","name":"Software Engineer","category":"Technology & Data","source":"onet",
     "description":"Design, build and maintain software systems and applications.",
     "ocean_profile":{"Openness":72,"Conscientiousness":82,"Extraversion":38,"Agreeableness":50,"Neuroticism":25},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"JEE (for CS degree pathway)",
     "work_style":["technical","systematic","independent"]},

    {"id":"ml_engineer","name":"Machine Learning Engineer","category":"Technology & Data","source":"onet",
     "description":"Build and deploy ML models and AI systems at scale.",
     "ocean_profile":{"Openness":85,"Conscientiousness":82,"Extraversion":35,"Agreeableness":48,"Neuroticism":20},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["analytical","technical","innovative"]},

    {"id":"ai_researcher","name":"AI Researcher","category":"Technology & Data","source":"onet",
     "description":"Conduct cutting-edge research in artificial intelligence and machine learning.",
     "ocean_profile":{"Openness":92,"Conscientiousness":82,"Extraversion":32,"Agreeableness":50,"Neuroticism":20},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["research","analytical","innovative"]},

    {"id":"cybersecurity_analyst","name":"Cybersecurity Analyst","category":"Technology & Data","source":"onet",
     "description":"Protect systems and networks from digital threats and attacks.",
     "ocean_profile":{"Openness":70,"Conscientiousness":88,"Extraversion":35,"Agreeableness":45,"Neuroticism":20},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["detail-oriented","vigilant","independent"]},

    {"id":"devops_engineer","name":"DevOps Engineer","category":"Technology & Data","source":"onet",
     "description":"Bridge development and operations to streamline software delivery pipelines.",
     "ocean_profile":{"Openness":72,"Conscientiousness":85,"Extraversion":40,"Agreeableness":55,"Neuroticism":22},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["technical","systematic","collaborative"]},

    {"id":"cloud_architect","name":"Cloud Architect","category":"Technology & Data","source":"onet",
     "description":"Design and manage cloud infrastructure for organisations at scale.",
     "ocean_profile":{"Openness":75,"Conscientiousness":85,"Extraversion":42,"Agreeableness":50,"Neuroticism":20},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["technical","strategic","systematic"]},

    {"id":"ux_designer","name":"UX/UI Designer","category":"Technology & Data","source":"onet",
     "description":"Design intuitive, user-centred digital interfaces and experiences.",
     "ocean_profile":{"Openness":88,"Conscientiousness":65,"Extraversion":58,"Agreeableness":72,"Neuroticism":35},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["creative","empathetic","collaborative"]},

    {"id":"product_manager","name":"Product Manager","category":"Technology & Data","source":"onet",
     "description":"Lead product vision, strategy and cross-functional execution.",
     "ocean_profile":{"Openness":78,"Conscientiousness":78,"Extraversion":70,"Agreeableness":65,"Neuroticism":28},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["strategic","communicative","leadership"]},

    {"id":"blockchain_developer","name":"Blockchain Developer","category":"Technology & Data","source":"onet",
     "description":"Build decentralised applications and smart contracts on blockchain platforms.",
     "ocean_profile":{"Openness":80,"Conscientiousness":82,"Extraversion":35,"Agreeableness":48,"Neuroticism":22},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["technical","innovative","independent"]},

    {"id":"data_engineer","name":"Data Engineer","category":"Technology & Data","source":"onet",
     "description":"Build and maintain data pipelines and infrastructure for analytics teams.",
     "ocean_profile":{"Openness":70,"Conscientiousness":85,"Extraversion":38,"Agreeableness":52,"Neuroticism":22},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["technical","systematic","analytical"]},

    {"id":"game_developer","name":"Game Developer","category":"Technology & Data","source":"onet",
     "description":"Design and build interactive games for mobile, PC and console platforms.",
     "ocean_profile":{"Openness":88,"Conscientiousness":72,"Extraversion":45,"Agreeableness":55,"Neuroticism":32},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["creative","technical","innovative"]},

    {"id":"it_consultant","name":"IT Consultant","category":"Technology & Data","source":"onet",
     "description":"Advise organisations on technology strategy and digital transformation.",
     "ocean_profile":{"Openness":75,"Conscientiousness":80,"Extraversion":68,"Agreeableness":62,"Neuroticism":25},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["strategic","communicative","analytical"]},

    # ── RESEARCH & ACADEMIA ──────────────────────────────────

    {"id":"research_scientist","name":"Research Scientist","category":"Research & Academia","source":"onet",
     "description":"Conduct original research to advance knowledge in a scientific field.",
     "ocean_profile":{"Openness":90,"Conscientiousness":80,"Extraversion":32,"Agreeableness":52,"Neuroticism":22},
     "user_types":["undergraduate","professional"],"entrance_exam":"GATE / CSIR-NET / JEST",
     "work_style":["analytical","curious","independent"]},

    {"id":"university_professor","name":"University Professor","category":"Research & Academia","source":"hybrid",
     "description":"Teach, mentor students and conduct research at a university.",
     "ocean_profile":{"Openness":88,"Conscientiousness":75,"Extraversion":60,"Agreeableness":68,"Neuroticism":25},
     "user_types":["undergraduate","professional"],"entrance_exam":"UGC-NET / PhD",
     "work_style":["intellectual","communicative","mentoring"]},

    {"id":"data_analyst","name":"Data Analyst","category":"Research & Academia","source":"onet",
     "description":"Interpret data and generate actionable business insights.",
     "ocean_profile":{"Openness":72,"Conscientiousness":82,"Extraversion":42,"Agreeableness":55,"Neuroticism":25},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["analytical","detail-oriented","systematic"]},

    {"id":"statistician","name":"Statistician","category":"Research & Academia","source":"onet",
     "description":"Apply statistical methods to collect, analyse and interpret data.",
     "ocean_profile":{"Openness":72,"Conscientiousness":85,"Extraversion":35,"Agreeableness":52,"Neuroticism":20},
     "user_types":["undergraduate","professional"],"entrance_exam":"CSIR-NET (Statistics)",
     "work_style":["analytical","precise","independent"]},

    {"id":"economist","name":"Economist","category":"Research & Academia","source":"onet",
     "description":"Study production, distribution and consumption of goods and services.",
     "ocean_profile":{"Openness":80,"Conscientiousness":78,"Extraversion":48,"Agreeableness":52,"Neuroticism":22},
     "user_types":["undergraduate","professional"],"entrance_exam":"IES / RBI Grade B",
     "work_style":["analytical","research-driven","systematic"]},

    {"id":"historian","name":"Historian / Archivist","category":"Research & Academia","source":"onet",
     "description":"Research and document historical events, cultures and societies.",
     "ocean_profile":{"Openness":88,"Conscientiousness":78,"Extraversion":38,"Agreeableness":60,"Neuroticism":28},
     "user_types":["undergraduate","professional"],"entrance_exam":"UGC-NET History",
     "work_style":["research-driven","detail-oriented","independent"]},

    # ── MEDICINE & HEALTH ────────────────────────────────────

    {"id":"doctor_mbbs","name":"Medical Doctor (MBBS)","category":"Medicine & Health","source":"indian",
     "description":"Diagnose and treat patients across clinical settings.",
     "ocean_profile":{"Openness":65,"Conscientiousness":90,"Extraversion":58,"Agreeableness":80,"Neuroticism":18},
     "user_types":["class_10","class_12"],"entrance_exam":"NEET-UG",
     "work_style":["caring","disciplined","high-stakes"]},

    {"id":"surgeon","name":"Surgeon","category":"Medicine & Health","source":"onet",
     "description":"Perform surgical procedures to treat disease, injury and deformity.",
     "ocean_profile":{"Openness":62,"Conscientiousness":95,"Extraversion":50,"Agreeableness":58,"Neuroticism":12},
     "user_types":["undergraduate","professional"],"entrance_exam":"NEET-PG / MS",
     "work_style":["precise","calm-under-pressure","technical"]},

    {"id":"psychiatrist","name":"Psychiatrist","category":"Medicine & Health","source":"onet",
     "description":"Diagnose and treat mental health disorders using therapy and medication.",
     "ocean_profile":{"Openness":80,"Conscientiousness":78,"Extraversion":55,"Agreeableness":85,"Neuroticism":28},
     "user_types":["undergraduate","professional"],"entrance_exam":"NEET-PG / MD Psychiatry",
     "work_style":["empathetic","analytical","patient"]},

    {"id":"physiotherapist","name":"Physiotherapist","category":"Medicine & Health","source":"hybrid",
     "description":"Rehabilitate patients with physical impairments through exercise and therapy.",
     "ocean_profile":{"Openness":62,"Conscientiousness":78,"Extraversion":62,"Agreeableness":85,"Neuroticism":28},
     "user_types":["class_12","undergraduate"],"entrance_exam":"NEET / BPT entrance",
     "work_style":["hands-on","caring","motivating"]},

    {"id":"dentist","name":"Dentist","category":"Medicine & Health","source":"indian",
     "description":"Diagnose and treat conditions affecting teeth, gums and oral health.",
     "ocean_profile":{"Openness":60,"Conscientiousness":88,"Extraversion":55,"Agreeableness":75,"Neuroticism":20},
     "user_types":["class_12","undergraduate"],"entrance_exam":"NEET-UG (BDS)",
     "work_style":["precise","caring","independent"]},

    {"id":"public_health_specialist","name":"Public Health Specialist","category":"Medicine & Health","source":"hybrid",
     "description":"Design and implement health programmes at community or national scale.",
     "ocean_profile":{"Openness":75,"Conscientiousness":75,"Extraversion":65,"Agreeableness":82,"Neuroticism":28},
     "user_types":["undergraduate","professional"],"entrance_exam":"MPH entrance / UPSC",
     "work_style":["strategic","collaborative","mission-driven"]},

    {"id":"radiologist","name":"Radiologist","category":"Medicine & Health","source":"onet",
     "description":"Interpret medical images to diagnose and guide treatment of disease.",
     "ocean_profile":{"Openness":65,"Conscientiousness":92,"Extraversion":40,"Agreeableness":60,"Neuroticism":18},
     "user_types":["undergraduate","professional"],"entrance_exam":"NEET-PG / MD Radiology",
     "work_style":["analytical","precise","independent"]},

    {"id":"nurse","name":"Nurse / Nursing Officer","category":"Medicine & Health","source":"indian",
     "description":"Provide direct patient care and coordinate health services in clinical settings.",
     "ocean_profile":{"Openness":60,"Conscientiousness":82,"Extraversion":62,"Agreeableness":88,"Neuroticism":28},
     "user_types":["class_12","undergraduate"],"entrance_exam":"B.Sc Nursing / AIIMS Nursing",
     "work_style":["caring","disciplined","collaborative"]},

    {"id":"nutritionist","name":"Dietitian / Nutritionist","category":"Medicine & Health","source":"onet",
     "description":"Advise individuals and organisations on diet, nutrition and healthy eating.",
     "ocean_profile":{"Openness":65,"Conscientiousness":78,"Extraversion":60,"Agreeableness":80,"Neuroticism":28},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["caring","systematic","communicative"]},

    # ── ENGINEERING ──────────────────────────────────────────

    {"id":"civil_engineer","name":"Civil Engineer","category":"Engineering","source":"hybrid",
     "description":"Design and oversee construction of infrastructure — roads, bridges, buildings.",
     "ocean_profile":{"Openness":60,"Conscientiousness":85,"Extraversion":50,"Agreeableness":58,"Neuroticism":22},
     "user_types":["class_12","undergraduate"],"entrance_exam":"JEE Main / JEE Advanced",
     "work_style":["systematic","practical","leadership"]},

    {"id":"mechanical_engineer","name":"Mechanical Engineer","category":"Engineering","source":"hybrid",
     "description":"Design and analyse mechanical systems, machines and thermal devices.",
     "ocean_profile":{"Openness":65,"Conscientiousness":85,"Extraversion":45,"Agreeableness":52,"Neuroticism":22},
     "user_types":["class_12","undergraduate"],"entrance_exam":"JEE Main / JEE Advanced",
     "work_style":["technical","systematic","problem-solving"]},

    {"id":"electrical_engineer","name":"Electrical Engineer","category":"Engineering","source":"hybrid",
     "description":"Design and develop electrical systems, circuits and power infrastructure.",
     "ocean_profile":{"Openness":68,"Conscientiousness":85,"Extraversion":42,"Agreeableness":50,"Neuroticism":22},
     "user_types":["class_12","undergraduate"],"entrance_exam":"JEE Main / GATE",
     "work_style":["analytical","precise","technical"]},

    {"id":"aerospace_engineer","name":"Aerospace Engineer","category":"Engineering","source":"onet",
     "description":"Design aircraft, spacecraft and related systems.",
     "ocean_profile":{"Openness":80,"Conscientiousness":88,"Extraversion":40,"Agreeableness":50,"Neuroticism":18},
     "user_types":["class_12","undergraduate"],"entrance_exam":"JEE Advanced / IIST entrance",
     "work_style":["innovative","precise","technical"]},

    {"id":"chemical_engineer","name":"Chemical Engineer","category":"Engineering","source":"onet",
     "description":"Design processes for producing, transforming and transporting chemicals.",
     "ocean_profile":{"Openness":70,"Conscientiousness":85,"Extraversion":42,"Agreeableness":52,"Neuroticism":22},
     "user_types":["class_12","undergraduate"],"entrance_exam":"JEE Main / JEE Advanced",
     "work_style":["analytical","systematic","technical"]},

    {"id":"robotics_engineer","name":"Robotics Engineer","category":"Engineering","source":"onet",
     "description":"Design, build and program robotic systems for automation and research.",
     "ocean_profile":{"Openness":82,"Conscientiousness":85,"Extraversion":38,"Agreeableness":50,"Neuroticism":20},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"JEE / GATE (ME/EE)",
     "work_style":["innovative","technical","systematic"]},

    {"id":"environmental_engineer","name":"Environmental Engineer","category":"Engineering","source":"onet",
     "description":"Develop solutions to environmental problems like pollution and waste management.",
     "ocean_profile":{"Openness":75,"Conscientiousness":80,"Extraversion":50,"Agreeableness":68,"Neuroticism":25},
     "user_types":["class_12","undergraduate"],"entrance_exam":"JEE / GATE (ENV)",
     "work_style":["mission-driven","systematic","field-based"]},

    {"id":"petroleum_engineer","name":"Petroleum Engineer","category":"Engineering","source":"onet",
     "description":"Design methods for extracting oil and gas from the earth efficiently.",
     "ocean_profile":{"Openness":65,"Conscientiousness":85,"Extraversion":48,"Agreeableness":50,"Neuroticism":20},
     "user_types":["class_12","undergraduate"],"entrance_exam":"JEE / ONGC recruitment",
     "work_style":["technical","field-based","analytical"]},

    {"id":"textile_engineer","name":"Textile Engineer","category":"Engineering","source":"indian",
     "description":"Develop and improve fibres, yarns, fabrics and textile processes.",
     "ocean_profile":{"Openness":62,"Conscientiousness":80,"Extraversion":45,"Agreeableness":55,"Neuroticism":25},
     "user_types":["class_12","undergraduate"],"entrance_exam":"JEE / NIFT (technical)",
     "work_style":["technical","detail-oriented","systematic"]},

    # ── BUSINESS & FINANCE ───────────────────────────────────

    {"id":"chartered_accountant","name":"Chartered Accountant (CA)","category":"Business & Finance","source":"indian",
     "description":"Manage financial reporting, auditing and taxation for organisations.",
     "ocean_profile":{"Openness":50,"Conscientiousness":92,"Extraversion":45,"Agreeableness":55,"Neuroticism":22},
     "user_types":["class_10","class_12","undergraduate"],"entrance_exam":"CA Foundation / ICAI",
     "work_style":["detail-oriented","rule-based","precise"]},

    {"id":"investment_banker","name":"Investment Banker","category":"Business & Finance","source":"onet",
     "description":"Raise capital, execute M&A deals and advise corporations on financial strategy.",
     "ocean_profile":{"Openness":68,"Conscientiousness":88,"Extraversion":72,"Agreeableness":48,"Neuroticism":22},
     "user_types":["undergraduate","professional"],"entrance_exam":"CAT / CFA / MBA",
     "work_style":["high-pressure","analytical","competitive"]},

    {"id":"financial_analyst","name":"Financial Analyst","category":"Business & Finance","source":"onet",
     "description":"Evaluate financial data to support investment and business decisions.",
     "ocean_profile":{"Openness":65,"Conscientiousness":85,"Extraversion":48,"Agreeableness":52,"Neuroticism":25},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"CFA / MBA Finance",
     "work_style":["analytical","systematic","research-driven"]},

    {"id":"entrepreneur","name":"Entrepreneur","category":"Business & Finance","source":"onet",
     "description":"Build and scale a business from idea to execution.",
     "ocean_profile":{"Openness":88,"Conscientiousness":72,"Extraversion":78,"Agreeableness":58,"Neuroticism":28},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["risk-tolerant","innovative","leadership"]},

    {"id":"management_consultant","name":"Management Consultant","category":"Business & Finance","source":"onet",
     "description":"Solve complex business problems and advise organisations on strategy.",
     "ocean_profile":{"Openness":78,"Conscientiousness":82,"Extraversion":72,"Agreeableness":60,"Neuroticism":22},
     "user_types":["undergraduate","professional"],"entrance_exam":"CAT / GMAT / MBA",
     "work_style":["analytical","communicative","structured"]},

    {"id":"actuary","name":"Actuary","category":"Business & Finance","source":"onet",
     "description":"Use mathematics and statistics to assess financial risk.",
     "ocean_profile":{"Openness":68,"Conscientiousness":90,"Extraversion":38,"Agreeableness":50,"Neuroticism":18},
     "user_types":["class_12","undergraduate"],"entrance_exam":"IAI / IFoA actuarial exams",
     "work_style":["quantitative","precise","independent"]},

    {"id":"marketing_manager","name":"Marketing Manager","category":"Business & Finance","source":"onet",
     "description":"Develop and execute marketing strategies to grow brand and revenue.",
     "ocean_profile":{"Openness":80,"Conscientiousness":72,"Extraversion":78,"Agreeableness":65,"Neuroticism":30},
     "user_types":["undergraduate","professional"],"entrance_exam":"CAT / MBA Marketing",
     "work_style":["creative","strategic","communicative"]},

    {"id":"hr_manager","name":"Human Resources Manager","category":"Business & Finance","source":"onet",
     "description":"Manage talent acquisition, development and employee relations.",
     "ocean_profile":{"Openness":68,"Conscientiousness":75,"Extraversion":72,"Agreeableness":85,"Neuroticism":28},
     "user_types":["undergraduate","professional"],"entrance_exam":"MBA HR / XLRI",
     "work_style":["people-focused","organised","communicative"]},

    {"id":"supply_chain_manager","name":"Supply Chain Manager","category":"Business & Finance","source":"onet",
     "description":"Oversee procurement, logistics and distribution networks end-to-end.",
     "ocean_profile":{"Openness":62,"Conscientiousness":88,"Extraversion":55,"Agreeableness":58,"Neuroticism":22},
     "user_types":["undergraduate","professional"],"entrance_exam":"MBA Operations",
     "work_style":["systematic","strategic","analytical"]},

    {"id":"stock_broker","name":"Stock Broker / Equity Analyst","category":"Business & Finance","source":"indian",
     "description":"Analyse securities and execute trades on behalf of clients or institutions.",
     "ocean_profile":{"Openness":68,"Conscientiousness":80,"Extraversion":68,"Agreeableness":48,"Neuroticism":28},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"NISM / SEBI certification",
     "work_style":["analytical","fast-paced","competitive"]},

    {"id":"real_estate","name":"Real Estate Developer / Agent","category":"Business & Finance","source":"hybrid",
     "description":"Buy, sell, develop and manage properties and land.",
     "ocean_profile":{"Openness":65,"Conscientiousness":75,"Extraversion":78,"Agreeableness":65,"Neuroticism":30},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["social","negotiation","entrepreneurial"]},

    # ── LAW & CIVIL SERVICES ─────────────────────────────────

    {"id":"ias_officer","name":"IAS / Civil Services Officer","category":"Law & Civil Services","source":"indian",
     "description":"Administer public policy and governance at district and national level.",
     "ocean_profile":{"Openness":75,"Conscientiousness":85,"Extraversion":65,"Agreeableness":68,"Neuroticism":18},
     "user_types":["undergraduate","professional"],"entrance_exam":"UPSC CSE",
     "work_style":["leadership","disciplined","mission-driven"]},

    {"id":"lawyer","name":"Lawyer / Advocate","category":"Law & Civil Services","source":"hybrid",
     "description":"Represent clients, argue cases and provide legal counsel.",
     "ocean_profile":{"Openness":75,"Conscientiousness":80,"Extraversion":72,"Agreeableness":55,"Neuroticism":28},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"CLAT / AILET",
     "work_style":["argumentative","analytical","communicative"]},

    {"id":"judge","name":"Judge","category":"Law & Civil Services","source":"hybrid",
     "description":"Preside over court proceedings and deliver impartial legal judgements.",
     "ocean_profile":{"Openness":70,"Conscientiousness":92,"Extraversion":50,"Agreeableness":60,"Neuroticism":12},
     "user_types":["professional"],"entrance_exam":"Judicial Services Exam / HJS",
     "work_style":["impartial","analytical","calm"]},

    {"id":"policy_analyst","name":"Policy Analyst","category":"Law & Civil Services","source":"onet",
     "description":"Research and evaluate public policies to inform government decisions.",
     "ocean_profile":{"Openness":82,"Conscientiousness":78,"Extraversion":55,"Agreeableness":65,"Neuroticism":25},
     "user_types":["undergraduate","professional"],"entrance_exam":"UPSC / State PSC",
     "work_style":["analytical","research-driven","mission-driven"]},

    {"id":"corporate_lawyer","name":"Corporate Lawyer","category":"Law & Civil Services","source":"hybrid",
     "description":"Handle mergers, acquisitions, contracts and corporate compliance.",
     "ocean_profile":{"Openness":70,"Conscientiousness":88,"Extraversion":60,"Agreeableness":52,"Neuroticism":22},
     "user_types":["undergraduate","professional"],"entrance_exam":"CLAT / LLB / LLM",
     "work_style":["analytical","high-pressure","strategic"]},

    {"id":"diplomat","name":"Diplomat / Foreign Service Officer","category":"Law & Civil Services","source":"indian",
     "description":"Represent India's interests abroad and manage international relations.",
     "ocean_profile":{"Openness":82,"Conscientiousness":80,"Extraversion":72,"Agreeableness":72,"Neuroticism":18},
     "user_types":["undergraduate","professional"],"entrance_exam":"UPSC IFS",
     "work_style":["diplomatic","communicative","strategic"]},

    # ── CREATIVE & MEDIA ─────────────────────────────────────

    {"id":"graphic_designer","name":"Graphic Designer","category":"Creative & Media","source":"onet",
     "description":"Create visual content for brands, media and digital platforms.",
     "ocean_profile":{"Openness":92,"Conscientiousness":60,"Extraversion":50,"Agreeableness":65,"Neuroticism":38},
     "user_types":["class_10","class_12","undergraduate","professional"],"entrance_exam":"NID / NIFT entrance",
     "work_style":["creative","visual","independent"]},

    {"id":"journalist","name":"Journalist","category":"Creative & Media","source":"onet",
     "description":"Investigate, report and communicate news and stories to the public.",
     "ocean_profile":{"Openness":85,"Conscientiousness":65,"Extraversion":75,"Agreeableness":60,"Neuroticism":38},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"IIMC / ACJ / Mass comm",
     "work_style":["curious","communicative","fast-paced"]},

    {"id":"filmmaker","name":"Filmmaker / Director","category":"Creative & Media","source":"onet",
     "description":"Conceptualise and direct films, web series and video content.",
     "ocean_profile":{"Openness":95,"Conscientiousness":65,"Extraversion":70,"Agreeableness":60,"Neuroticism":42},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"FTII / SRFTI entrance",
     "work_style":["creative","visionary","collaborative"]},

    {"id":"content_writer","name":"Content Writer / Author","category":"Creative & Media","source":"onet",
     "description":"Create written content for digital, print and broadcast media.",
     "ocean_profile":{"Openness":88,"Conscientiousness":60,"Extraversion":42,"Agreeableness":62,"Neuroticism":40},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["creative","independent","reflective"]},

    {"id":"architect","name":"Architect","category":"Creative & Media","source":"onet",
     "description":"Design buildings and spaces that are functional, safe and aesthetically compelling.",
     "ocean_profile":{"Openness":88,"Conscientiousness":80,"Extraversion":52,"Agreeableness":60,"Neuroticism":30},
     "user_types":["class_12","undergraduate"],"entrance_exam":"NATA / JEE Paper 2",
     "work_style":["creative","technical","detail-oriented"]},

    {"id":"photographer","name":"Photographer / Videographer","category":"Creative & Media","source":"onet",
     "description":"Capture and edit visual stories through photography and video.",
     "ocean_profile":{"Openness":90,"Conscientiousness":58,"Extraversion":55,"Agreeableness":65,"Neuroticism":38},
     "user_types":["class_10","class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["creative","visual","independent"]},

    {"id":"fashion_designer","name":"Fashion Designer","category":"Creative & Media","source":"onet",
     "description":"Design clothing, accessories and fashion collections.",
     "ocean_profile":{"Openness":92,"Conscientiousness":62,"Extraversion":62,"Agreeableness":60,"Neuroticism":38},
     "user_types":["class_10","class_12","undergraduate"],"entrance_exam":"NIFT / NID entrance",
     "work_style":["creative","visual","entrepreneurial"]},

    {"id":"musician","name":"Musician / Music Producer","category":"Creative & Media","source":"onet",
     "description":"Compose, perform and produce music across genres and formats.",
     "ocean_profile":{"Openness":92,"Conscientiousness":58,"Extraversion":65,"Agreeableness":68,"Neuroticism":42},
     "user_types":["class_10","class_12","undergraduate","professional"],"entrance_exam":"Music college auditions",
     "work_style":["creative","expressive","independent"]},

    {"id":"animator","name":"Animator / Motion Designer","category":"Creative & Media","source":"onet",
     "description":"Create animated visuals for films, games, advertising and digital media.",
     "ocean_profile":{"Openness":90,"Conscientiousness":68,"Extraversion":45,"Agreeableness":60,"Neuroticism":35},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"Arena / MAAC / DSK",
     "work_style":["creative","technical","detail-oriented"]},

    {"id":"art_director","name":"Art Director","category":"Creative & Media","source":"onet",
     "description":"Lead the visual direction for advertising, publishing or media productions.",
     "ocean_profile":{"Openness":90,"Conscientiousness":68,"Extraversion":62,"Agreeableness":60,"Neuroticism":35},
     "user_types":["undergraduate","professional"],"entrance_exam":"NID / NIFT / Portfolio",
     "work_style":["creative","leadership","strategic"]},

    {"id":"copywriter","name":"Copywriter / Creative Director","category":"Creative & Media","source":"onet",
     "description":"Write compelling copy for advertising, branding and marketing campaigns.",
     "ocean_profile":{"Openness":88,"Conscientiousness":62,"Extraversion":60,"Agreeableness":62,"Neuroticism":38},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["creative","strategic","communicative"]},

    # ── EDUCATION & SOCIAL IMPACT ────────────────────────────

    {"id":"school_teacher","name":"School Teacher","category":"Education & Social Impact","source":"hybrid",
     "description":"Educate and mentor students at primary or secondary school level.",
     "ocean_profile":{"Openness":68,"Conscientiousness":72,"Extraversion":68,"Agreeableness":85,"Neuroticism":32},
     "user_types":["class_12","undergraduate"],"entrance_exam":"B.Ed / CTET / TET",
     "work_style":["nurturing","patient","communicative"]},

    {"id":"social_worker","name":"Social Worker / NGO Professional","category":"Education & Social Impact","source":"onet",
     "description":"Support individuals and communities facing social, economic or health challenges.",
     "ocean_profile":{"Openness":72,"Conscientiousness":68,"Extraversion":65,"Agreeableness":90,"Neuroticism":38},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"MSW entrance",
     "work_style":["empathetic","mission-driven","collaborative"]},

    {"id":"psychologist","name":"Psychologist / Counsellor","category":"Education & Social Impact","source":"onet",
     "description":"Assess and support individuals with mental, emotional and behavioural challenges.",
     "ocean_profile":{"Openness":80,"Conscientiousness":72,"Extraversion":58,"Agreeableness":88,"Neuroticism":30},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"MA Psychology / RCI",
     "work_style":["empathetic","analytical","patient"]},

    {"id":"career_counsellor","name":"Career Counsellor","category":"Education & Social Impact","source":"hybrid",
     "description":"Guide students and professionals through career decisions and transitions.",
     "ocean_profile":{"Openness":75,"Conscientiousness":72,"Extraversion":70,"Agreeableness":88,"Neuroticism":28},
     "user_types":["undergraduate","professional"],"entrance_exam":"M.Ed / Counselling certification",
     "work_style":["empathetic","communicative","mentoring"]},

    {"id":"special_educator","name":"Special Educator","category":"Education & Social Impact","source":"onet",
     "description":"Teach and support students with learning disabilities and special needs.",
     "ocean_profile":{"Openness":70,"Conscientiousness":75,"Extraversion":62,"Agreeableness":92,"Neuroticism":30},
     "user_types":["class_12","undergraduate"],"entrance_exam":"B.Ed Special Education / RCI",
     "work_style":["nurturing","patient","adaptive"]},

    {"id":"development_sector","name":"Development Sector Professional","category":"Education & Social Impact","source":"hybrid",
     "description":"Work on international development, poverty alleviation and social programmes.",
     "ocean_profile":{"Openness":80,"Conscientiousness":72,"Extraversion":65,"Agreeableness":85,"Neuroticism":30},
     "user_types":["undergraduate","professional"],"entrance_exam":"IRMA / Tata Institute / IIFM",
     "work_style":["mission-driven","collaborative","strategic"]},

    # ── DEFENCE & GOVERNMENT ─────────────────────────────────

    {"id":"army_officer","name":"Army Officer","category":"Defence & Government","source":"indian",
     "description":"Lead military operations and manage personnel in the Indian Army.",
     "ocean_profile":{"Openness":55,"Conscientiousness":90,"Extraversion":70,"Agreeableness":60,"Neuroticism":10},
     "user_types":["class_12","undergraduate"],"entrance_exam":"NDA / CDS / AFCAT",
     "work_style":["leadership","disciplined","high-stakes"]},

    {"id":"police_officer","name":"Police Officer / IPS","category":"Defence & Government","source":"indian",
     "description":"Enforce law, investigate crimes and maintain public order.",
     "ocean_profile":{"Openness":58,"Conscientiousness":85,"Extraversion":65,"Agreeableness":58,"Neuroticism":15},
     "user_types":["undergraduate","professional"],"entrance_exam":"UPSC CSE (IPS) / State PSC",
     "work_style":["assertive","disciplined","adaptive"]},

    {"id":"navy_officer","name":"Navy Officer","category":"Defence & Government","source":"indian",
     "description":"Serve in the Indian Navy managing naval operations and personnel.",
     "ocean_profile":{"Openness":58,"Conscientiousness":88,"Extraversion":65,"Agreeableness":58,"Neuroticism":12},
     "user_types":["class_12","undergraduate"],"entrance_exam":"NDA / CDSE / SSB",
     "work_style":["disciplined","leadership","technical"]},

    {"id":"ifs_officer","name":"Indian Forest Service (IFS) Officer","category":"Defence & Government","source":"indian",
     "description":"Manage and conserve India's forests, wildlife and natural resources.",
     "ocean_profile":{"Openness":72,"Conscientiousness":82,"Extraversion":55,"Agreeableness":70,"Neuroticism":20},
     "user_types":["undergraduate","professional"],"entrance_exam":"UPSC IFS",
     "work_style":["field-based","mission-driven","disciplined"]},

    {"id":"rbi_officer","name":"RBI / Banking Officer (IBPS)","category":"Defence & Government","source":"indian",
     "description":"Manage monetary policy, banking operations or financial regulation.",
     "ocean_profile":{"Openness":60,"Conscientiousness":88,"Extraversion":52,"Agreeableness":58,"Neuroticism":20},
     "user_types":["undergraduate","professional"],"entrance_exam":"RBI Grade B / IBPS PO",
     "work_style":["systematic","analytical","disciplined"]},

    # ── SCIENCE & ENVIRONMENT ────────────────────────────────

    {"id":"environmental_scientist","name":"Environmental Scientist","category":"Science & Environment","source":"onet",
     "description":"Study the environment and develop solutions to ecological problems.",
     "ocean_profile":{"Openness":82,"Conscientiousness":75,"Extraversion":48,"Agreeableness":70,"Neuroticism":28},
     "user_types":["class_12","undergraduate"],"entrance_exam":"GATE (Environmental) / IFS",
     "work_style":["curious","mission-driven","field-based"]},

    {"id":"biotechnologist","name":"Biotechnologist","category":"Science & Environment","source":"hybrid",
     "description":"Apply biology and technology to develop products in medicine, agriculture and industry.",
     "ocean_profile":{"Openness":82,"Conscientiousness":82,"Extraversion":40,"Agreeableness":55,"Neuroticism":22},
     "user_types":["class_12","undergraduate"],"entrance_exam":"NEET / JEE / GATE (BT)",
     "work_style":["analytical","curious","lab-based"]},

    {"id":"pharmacist","name":"Pharmacist","category":"Science & Environment","source":"onet",
     "description":"Dispense medication and counsel patients on drug use and interactions.",
     "ocean_profile":{"Openness":60,"Conscientiousness":88,"Extraversion":55,"Agreeableness":75,"Neuroticism":22},
     "user_types":["class_12","undergraduate"],"entrance_exam":"NEET / B.Pharm entrance",
     "work_style":["precise","caring","systematic"]},

    {"id":"geologist","name":"Geologist","category":"Science & Environment","source":"onet",
     "description":"Study the Earth's structure, composition and geological processes.",
     "ocean_profile":{"Openness":80,"Conscientiousness":78,"Extraversion":42,"Agreeableness":55,"Neuroticism":22},
     "user_types":["class_12","undergraduate"],"entrance_exam":"GATE (GG) / GSI recruitment",
     "work_style":["curious","field-based","analytical"]},

    {"id":"astrophysicist","name":"Astrophysicist / Astronomer","category":"Science & Environment","source":"onet",
     "description":"Study celestial objects, space and the physical universe.",
     "ocean_profile":{"Openness":95,"Conscientiousness":80,"Extraversion":32,"Agreeableness":52,"Neuroticism":20},
     "user_types":["class_12","undergraduate"],"entrance_exam":"JEST / ISRO / IIA recruitment",
     "work_style":["curious","analytical","independent"]},

    {"id":"marine_biologist","name":"Marine Biologist","category":"Science & Environment","source":"onet",
     "description":"Study ocean ecosystems, marine organisms and underwater environments.",
     "ocean_profile":{"Openness":88,"Conscientiousness":72,"Extraversion":48,"Agreeableness":68,"Neuroticism":28},
     "user_types":["class_12","undergraduate"],"entrance_exam":"CSIR-NET / ICAR / NIO",
     "work_style":["curious","field-based","mission-driven"]},

    {"id":"agricultural_scientist","name":"Agricultural Scientist","category":"Science & Environment","source":"indian",
     "description":"Research and improve crop production, soil health and farming practices.",
     "ocean_profile":{"Openness":72,"Conscientiousness":78,"Extraversion":50,"Agreeableness":68,"Neuroticism":25},
     "user_types":["class_12","undergraduate"],"entrance_exam":"ICAR AIEEA / PAU / IARI",
     "work_style":["field-based","systematic","mission-driven"]},

    # ── HOSPITALITY, SPORTS & WELLNESS ──────────────────────

    {"id":"hotel_manager","name":"Hotel / Hospitality Manager","category":"Hospitality & Sports","source":"onet",
     "description":"Oversee hotel operations and ensure exceptional guest experiences.",
     "ocean_profile":{"Openness":65,"Conscientiousness":78,"Extraversion":80,"Agreeableness":80,"Neuroticism":28},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"IHM entrance / NCHMCT JEE",
     "work_style":["service-oriented","leadership","social"]},

    {"id":"sports_coach","name":"Sports Coach / Athlete","category":"Hospitality & Sports","source":"onet",
     "description":"Train athletes and develop sports programmes at competitive levels.",
     "ocean_profile":{"Openness":62,"Conscientiousness":80,"Extraversion":75,"Agreeableness":68,"Neuroticism":22},
     "user_types":["class_10","class_12","undergraduate"],"entrance_exam":"NIS Patiala / SAI",
     "work_style":["motivating","disciplined","energetic"]},

    {"id":"yoga_instructor","name":"Yoga Instructor / Wellness Coach","category":"Hospitality & Sports","source":"hybrid",
     "description":"Guide individuals through physical and mental wellness practices.",
     "ocean_profile":{"Openness":72,"Conscientiousness":65,"Extraversion":62,"Agreeableness":85,"Neuroticism":22},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":"Yoga certification / AYUSH",
     "work_style":["caring","mindful","independent"]},

    {"id":"event_manager","name":"Event Manager","category":"Hospitality & Sports","source":"onet",
     "description":"Plan, coordinate and execute large-scale events, conferences and productions.",
     "ocean_profile":{"Openness":72,"Conscientiousness":80,"Extraversion":82,"Agreeableness":68,"Neuroticism":30},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["social","organised","high-pressure"]},

    {"id":"travel_consultant","name":"Travel Consultant / Tour Operator","category":"Hospitality & Sports","source":"onet",
     "description":"Plan and sell travel experiences for individuals and groups.",
     "ocean_profile":{"Openness":78,"Conscientiousness":70,"Extraversion":78,"Agreeableness":72,"Neuroticism":30},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["social","creative","entrepreneurial"]},

    # ── STREAM GUIDANCE (Class 10) ───────────────────────────

    {"id":"stream_science","name":"Science Stream (PCM / PCB)","category":"Stream Selection","source":"indian",
     "description":"Foundation for engineering, medicine, research and technology careers.",
     "ocean_profile":{"Openness":72,"Conscientiousness":80,"Extraversion":42,"Agreeableness":52,"Neuroticism":25},
     "user_types":["class_10"],"entrance_exam":"JEE / NEET (after 12th)",
     "work_style":["analytical","systematic","curious"]},

    {"id":"stream_commerce","name":"Commerce Stream","category":"Stream Selection","source":"indian",
     "description":"Foundation for finance, business, law and economics careers.",
     "ocean_profile":{"Openness":58,"Conscientiousness":80,"Extraversion":58,"Agreeableness":60,"Neuroticism":28},
     "user_types":["class_10"],"entrance_exam":"CA Foundation / CLAT / CAT (after degree)",
     "work_style":["structured","social","goal-oriented"]},

    {"id":"stream_arts","name":"Arts / Humanities Stream","category":"Stream Selection","source":"indian",
     "description":"Foundation for social sciences, law, journalism, design and creative careers.",
     "ocean_profile":{"Openness":88,"Conscientiousness":60,"Extraversion":62,"Agreeableness":75,"Neuroticism":38},
     "user_types":["class_10"],"entrance_exam":"CLAT / UPSC / Mass comm (after 12th)",
     "work_style":["creative","communicative","empathetic"]},

    # ── EMERGING & FREELANCE ─────────────────────────────────

    {"id":"social_media_manager","name":"Social Media Manager","category":"Creative & Media","source":"onet",
     "description":"Build and manage brand presence across social media platforms.",
     "ocean_profile":{"Openness":80,"Conscientiousness":65,"Extraversion":80,"Agreeableness":68,"Neuroticism":32},
     "user_types":["class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["creative","social","fast-paced"]},

    {"id":"edtech_professional","name":"EdTech Professional","category":"Education & Social Impact","source":"hybrid",
     "description":"Build and deliver digital learning products and educational technology solutions.",
     "ocean_profile":{"Openness":80,"Conscientiousness":72,"Extraversion":62,"Agreeableness":72,"Neuroticism":28},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["innovative","mission-driven","collaborative"]},

    {"id":"startup_founder","name":"Startup Founder / Co-founder","category":"Business & Finance","source":"onet",
     "description":"Ideate, build and grow a startup from zero to scale.",
     "ocean_profile":{"Openness":90,"Conscientiousness":75,"Extraversion":80,"Agreeableness":58,"Neuroticism":30},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["risk-tolerant","visionary","leadership"]},

    {"id":"ngo_founder","name":"NGO Founder / Social Entrepreneur","category":"Education & Social Impact","source":"hybrid",
     "description":"Build organisations that address social, environmental and community problems.",
     "ocean_profile":{"Openness":85,"Conscientiousness":70,"Extraversion":72,"Agreeableness":88,"Neuroticism":30},
     "user_types":["undergraduate","professional"],"entrance_exam":None,
     "work_style":["mission-driven","leadership","collaborative"]},

    {"id":"content_creator","name":"Content Creator / Influencer","category":"Creative & Media","source":"onet",
     "description":"Build and monetise an audience through video, blogs or social media content.",
     "ocean_profile":{"Openness":85,"Conscientiousness":58,"Extraversion":82,"Agreeableness":65,"Neuroticism":38},
     "user_types":["class_10","class_12","undergraduate","professional"],"entrance_exam":None,
     "work_style":["creative","entrepreneurial","social"]},
]

CAREER_LOOKUP = {c['id']: c for c in CAREERS}
CATEGORIES    = sorted(set(c['category'] for c in CAREERS))