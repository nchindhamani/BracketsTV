"""
BracketsTV Configuration Data
==============================

This module contains the master data structures for BracketsTV:
- MASTER_CHANNEL_LIST: All YouTube channels used in the application
- APP_CONFIG: Complete configuration for all categories and subcategories

This data serves as the "source of truth" for the seed.py script.
"""

# ==============================================================================
# MASTER DATA FOR BRACKETSTV
# ==============================================================================

# 1. A master list of all unique channels to avoid repetition.
MASTER_CHANNEL_LIST = {
    # DSA
    "NeetCode": {"channel_id": "UC_mYaQAE6-71g0JCo9cCMUA", "channel_handle": "@NeetCodeio"},
    "freeCodeCamp.org": {"channel_id": "UC8butISFwT-Wl7EV0hUK0BQ", "channel_handle": "@freecodecamp"},
    "Abdul Bari": {"channel_id": "UCZCFT11CWBi3MHNlGf019nw", "channel_handle": "@abdul_bari"},
    "CS Dojo": {"channel_id": "UCxX9wt5FWQUAAz4UrysqK9A", "channel_handle": "@CSDojo"},
    "Back To Back SWE": {"channel_id": "UCmJz2DV1a3yfgrR7GqRtUUA", "channel_handle": "@BackToBackSWE"},
    "WilliamFiset": {"channel_id": "UCD8-slMDTU3zddW_eXjhUjg", "channel_handle": "@WilliamFiset-videos"},
    "Errichto": {"channel_id": "UCdJt_D2i4i-y5WEi1sbs9gA", "channel_handle": "@Errichto"},
    "AlgoEngine": {"channel_id": "UCk-HsyV3K-g-46LD7H-i9bA", "channel_handle": "@AlgoEngine"},
    "Gaurav Sen": {"channel_id": "UCRPMAqdtSgd0IPEef7iMqVg", "channel_handle": "@GauravSensei"},
    "mycodeschool": {"channel_id": "UClEEsT7Dkdt2btmOFY1u_vA", "channel_handle": "@mycodeschool"},
    "Tech With Tim": {"channel_id": "UC4JXvGtOQzssDyYgemNl_-A", "channel_handle": "@TechWithTim"},
    "Clément Mihailescu": {"channel_id": "UCaO6VoaYJv4kS-TQO_M-N_g", "channel_handle": "@ClementMihailescu"},
    "Nick White": {"channel_id": "UC1fLEeYhtVLFaW4HD9lBhMw", "channel_handle": "@NickWhite"},
    "Joma Tech": {"channel_id": "UCV0qA-eDDICsRR9rPcnG7tw", "channel_handle": "@JomaTech"},
    
    # System Design
    "ByteByteGo": {"channel_id": "UCZgt6AzoyjslHTC9dz0UoTw", "channel_handle": "@ByteByteGo"},
    "Exponent": {"channel_id": "UCM2M-B-1s0D-sdG3A0sC-UA", "channel_handle": "@tryexponent"},
    "Jordan Has No Life": {"channel_id": "UCn-3W4THeitQc8N_wS1-cMg", "channel_handle": "@JordanHasNoLife"},
    "Hussein Nasser": {"channel_id": "UC_ML5xP23TOWKzIMy_jA0EA", "channel_handle": "@hnasr"},
    "CodeKarle": {"channel_id": "UCptXsp_NGh_eKk-bA3-3AZA", "channel_handle": "@codekarle"},
    "InfoQ": {"channel_id": "UCkQX1_yj5HH0aH39qa3sOwg", "channel_handle": "@InfoQ"},
    "Uber Engineering": {"channel_id": "UCvwoP_t_3-pT2a_3A6fJvPg", "channel_handle": "@UberEng"},
    "Netflix Engineering": {"channel_id": "UC364g_2q0a-m1T33_yM6z2g", "channel_handle": "@NetflixEng"},
    "Meta Engineering": {"channel_id": "UCsTqB7hY13nJ0v3s2S6-S_g", "channel_handle": "@MetaEng"},
    "Tushar Roy": {"channel_id": "UCn1XnDWhsLS5URXTi5p2T3A", "channel_handle": "@tusharroy"},
    
    # Behavioral
    "Dan Croitor": {"channel_id": "UCwPZ03-xYg91I-lD0-j-25A", "channel_handle": "@dancroitor"},
    "A Life After Layoff": {"channel_id": "UCPww4jCoGj-5C-l_2-s0-Yw", "channel_handle": "@alifeafterlayoff"},
    "Linda Raynier": {"channel_id": "UC-bF-gS6v3vO-0_8PNDV35g", "channel_handle": "@LindaRaynier"},
    "Jeff H Sipe": {"channel_id": "UCSC089-aO1-8sIL-s2EaTvQ", "channel_handle": "@JeffHSipe"},
    "Self Made Millennial": {"channel_id": "UCi2t-bL34uW4-s3tJp24bBw", "channel_handle": "@SelfMadeMillennial"},
    "Andrew LaCivita": {"channel_id": "UC_n9aD234S1PfZKMd9gKNOg", "channel_handle": "@ALC"},
    "CareerVidz": {"channel_id": "UC_aFtrLCRG-wB-1v-x2_23Q", "channel_handle": "@CareerVidz"},
    "The Companies Expert": {"channel_id": "UC7hPMp1u5Y7-1-t6h5g237Q", "channel_handle": "@TheCompaniesExpert"},

    # Languages
    "Programming with Mosh": {"channel_id": "UCWv7vFStA_juaYSq-cKVXgQ", "channel_handle": "@programmingwithmosh"},
    "The Net Ninja": {"channel_id": "UCW5YeuERMmlnqo4oq8vwUpg", "channel_handle": "@TheNetNinja"},
    "Corey Schafer": {"channel_id": "UCO1cgjhGdkAQbckDgocLiwQ", "channel_handle": "@coreyms"},
    "Fireship": {"channel_id": "UCsBjURrPoezykLs9EqgamOA", "channel_handle": "@Fireship"},
    "The Cherno": {"channel_id": "UCQ-W1lsa9k2y_eStkL7esWg", "channel_handle": "@TheCherno"},
    "IAmTimCorey": {"channel_id": "UC-ptHt4v1SRE7Ea3OAmlHtg", "channel_handle": "@IAmTimCorey"},
    "Philipp Lackner": {"channel_id": "UCKNTZMRHPLXfqlbdOI7mCkg", "channel_handle": "@PhilippLackner"},
    "CodeWithChris": {"channel_id": "UC2D6eRvCeMtcF5OGHf1-trw", "channel_handle": "@CodeWithChris"},
    "Paul Hudson": {"channel_id": "UCmJi5g_2K6D0kcFxJmC4viA", "channel_handle": "@twostraws"},
    "Bro Code": {"channel_id": "UCm-J8s_h4_c-kImk1jAk_yQ", "channel_handle": "@BroCodez"},
    "Telusko": {"channel_id": "UC59K-uG2A5ogwIrHw4bmlEg", "channel_handle": "@telusko"},
    "Jason Turner": {"channel_id": "UC_2C-L7-yE-P70k2L29b_1w", "channel_handle": "@JasonTurner-lefticus"},
    "CodeBeauty": {"channel_id": "UCM5_FkG3evj2wDlrW-5g3gQ", "channel_handle": "@CodeBeauty"},
    "JustForFunc": {"channel_id": "UC_n_3wGpi-O3kPZ3uF2a4uQ", "channel_handle": "@justforfunc"},
    "Anthony GG": {"channel_id": "UCnUURb2j_nRB_g_37voa-wA", "channel_handle": "@anthonygg_"},
    "Let's Get Rusty": {"channel_id": "UCpeX4D-ArTrsqOKAnA3Fhjg", "channel_handle": "@LetsGetRusty"},
    "Alex The Analyst": {"channel_id": "UC7cs8q-gKxS_q6CTeJgOtaA", "channel_handle": "@AlexTheAnalyst"},
    "kudvenkat": {"channel_id": "UCBH3-hFwW7B7t2Iu_2L2T9w", "channel_handle": "@kudvenkat"},
    "CodingWithMitch": {"channel_id": "UCoNZZLhPuuRteu02rh7bzsw", "channel_handle": "@codingwithmitch"},
    "Sean Allen": {"channel_id": "UCuP2vJ6kRutQBfRmdcI92mA", "channel_handle": "@seanallen"},
    "Jack Herrington": {"channel_id": "UC6vRUjYqD_v7I2KRJ3I-w-Q", "channel_handle": "@jherr"},
    "Nick Chapsas": {"channel_id": "UCLoCTfAXDk_e_6a9T27e24A", "channel_handle": "@nickchapsas"},
    "JetBrains TV": {"channel_id": "UC4z99vJg6t0s3g2B4iIqV-g", "channel_handle": "@JetBrainsTV"},
    "Traversy Media": {"channel_id": "UC29ju8bIqX1iPOyG6CgBwQA", "channel_handle": "@TraversyMedia"},
    "No Boilerplate": {"channel_id": "UC2R2d-iSRv114d7c6bYwW2A", "channel_handle": "@NoBoilerplate"},
    "Ryan Levick": {"channel_id": "UCi39b_aZk-2cQGF0-p-d_XQ", "channel_handle": "@ryanlevick"},
    "Learn To Code": {"channel_id": "UCu-YpQ7PA8I2O00a-bL3X-Q", "channel_handle": "@Learn-to-Code"},
    "LetsBuildThatApp": {"channel_id": "UCuWeq9L43N0cpyP_C3I4J2g", "channel_handle": "@LetsBuildThatApp"},
    "Amigoscode": {"channel_id": "UC2KfmYEM4KCuA1ZurravgYw", "channel_handle": "@amigoscode"},
    "Nic Jackson": {"channel_id": "UCxw2EbkvGCfGKcDu-nGp6Fw", "channel_handle": "@nicjackson"},
    "James Q Quick": {"channel_id": "UC-T8W79DN6PBnzomelvqJYw", "channel_handle": "@JamesQQuick"},
    
    # AI & ML
    "Two Minute Papers": {"channel_id": "UCbfYPyITQ-7l4upoX8nvctg", "channel_handle": "@TwoMinutePapers"},
    "Andrej Karpathy": {"channel_id": "UC_SSlF8s_pJ33gV2B2tM04Q", "channel_handle": "@AndrejKarpathy"},
    "StatQuest with Josh Starmer": {"channel_id": "UCtYLUTtgS3k1Fg4y5tAhLbw", "channel_handle": "@statquest"},
    "Yannic Kilcher": {"channel_id": "UCZHmQk67mSJgfCCTn7xBfew", "channel_handle": "@YannicKilcher"},
    "Sentdex": {"channel_id": "UCfzlCWGWYyIQ0aLC5w48gBQ", "channel_handle": "@sentdex"},
    "Lex Fridman": {"channel_id": "UCSHZKyawb77ixDdsGog4iWA", "channel_handle": "@lexfridman"},
    "DeepLearning.AI": {"channel_id": "UCkDaE8uoyJtq06R1n1PC-JQ", "channel_handle": "@Deeplearningai"},
    "LangChain": {"channel_id": "UCC-d1_n_Kzao-h_u-d_T_Yg", "channel_handle": "@LangChain"},
    
    # Dev Productivity
    "ThePrimeTime": {"channel_id": "UC-0t2-520dpIokw0T5qL-yA", "channel_handle": "@ThePrimeTimeagen"},
    "Docker": {"channel_id": "UC-3w_2B7jjAAI0k93Ietj1A", "channel_handle": "@DockerInc"},
    "Jeff Geerling": {"channel_id": "UCR-8O-Mup6e4aV03a2rltAw", "channel_handle": "@JeffGeerling"},
    "Theo - t3.gg": {"channel_id": "UCbRP3c757lq3jz76bNmm2Xg", "channel_handle": "@t3dotgg"},
    "GitKraken": {"channel_id": "UCp-JnB22oh-Phd722kZH7yA", "channel_handle": "@GitKraken"},
    "KodeKloud": {"channel_id": "UC2y3uhwff3xEU39o6_DTgBA", "channel_handle": "@KodeKloud"},
}

# 2. The main configuration for the app.
APP_CONFIG = [
    {
        "main_category": "dsa",
        "subcategories": [
            {"name": "Most Watched", "strategy": "POPULARITY", "search_query": "data structures OR algorithms tutorial", "is_active": True, "channels": []},
            {"name": "Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "data structures OR algorithms", "is_active": True, "channels": ["NeetCode", "freeCodeCamp.org", "Abdul Bari", "CS Dojo", "Back To Back SWE", "WilliamFiset", "Errichto", "AlgoEngine", "Gaurav Sen", "mycodeschool", "Tech With Tim", "Clément Mihailescu", "Nick White", "Joma Tech"]},
            {"name": "Quick Concepts (Under 20 mins)", "strategy": "FORMAT_DURATION", "search_query": "data structures OR algorithms", "is_active": True, "channels": []},
            {"name": "Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "(data structures OR algorithms) masterclass", "is_active": True, "channels": []},
            {"name": "Arrays & Strings", "strategy": "TOPIC_CURATED", "search_query": "(arrays OR strings) AND (data structures OR algorithms)", "is_active": True, "channels": ["NeetCode", "freeCodeCamp.org", "CS Dojo", "Back To Back SWE", "Gaurav Sen", "mycodeschool"]},
            {"name": "Linked Lists", "strategy": "TOPIC_CURATED", "search_query": "'linked lists' AND (data structures OR algorithms)", "is_active": True, "channels": ["NeetCode", "freeCodeCamp.org", "CS Dojo", "mycodeschool"]},
            {"name": "Searching & Sorting", "strategy": "TOPIC_CURATED", "search_query": "(searching OR sorting) AND algorithms", "is_active": True, "channels": ["NeetCode", "freeCodeCamp.org", "CS Dojo", "mycodeschool", "Abdul Bari"]},
            {"name": "Trees & Graphs", "strategy": "TOPIC_CURATED", "search_query": "(trees OR graphs) AND (data structures OR algorithms)", "is_active": True, "channels": ["NeetCode", "freeCodeCamp.org", "CS Dojo", "Back To Back SWE", "WilliamFiset", "Abdul Bari"]},
            {"name": "Heaps & Tries", "strategy": "TOPIC_CURATED", "search_query": "(heaps OR tries OR 'priority queue') AND (data structures OR algorithms)", "is_active": True, "channels": ["NeetCode", "freeCodeCamp.org", "WilliamFiset", "Abdul Bari"]},
            {"name": "Dynamic Programming", "strategy": "TOPIC_CURATED", "search_query": "'dynamic programming' AND algorithms", "is_active": True, "channels": ["NeetCode", "freeCodeCamp.org", "CS Dojo", "Back To Back SWE", "Errichto"]},
            {"name": "Backtracking", "strategy": "TOPIC_CURATED", "search_query": "backtracking AND algorithms", "is_active": True, "channels": ["NeetCode", "freeCodeCamp.org", "Back To Back SWE"]},
        ]
    },
    {
        "main_category": "system_design",
        "subcategories": [
             {"name": "Most Watched", "strategy": "POPULARITY", "search_query": "system design interview", "is_active": True, "channels": []},
             {"name": "Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "system design", "is_active": True, "channels": ["ByteByteGo", "Gaurav Sen", "Exponent", "Jordan Has No Life", "Hussein Nasser", "CodeKarle", "InfoQ"]},
             {"name": "Masterclasses & Deep Dives", "strategy": "FORMAT_KEYWORD", "search_query": "'system design' (masterclass OR 'deep dive' OR course)", "is_active": True, "channels": ["ByteByteGo", "Gaurav Sen", "Hussein Nasser"]},
             {"name": "System Design Fundamentals", "strategy": "TOPIC_CURATED", "search_query": "system design fundamentals (scalability OR caching OR database OR 'load balancer')", "is_active": True, "channels": ["ByteByteGo", "Gaurav Sen", "Exponent", "Hussein Nasser", "CodeKarle"]},
             {"name": "Full Mock Interviews", "strategy": "FORMAT_KEYWORD", "search_query": "'system design mock interview'", "is_active": True, "channels": ["Exponent", "Jordan Has No Life", "Gaurav Sen"]},
        ]
    },
    {
        "main_category": "behavioral",
        "subcategories": [
            {"name": "Most Watched", "strategy": "POPULARITY", "search_query": "behavioral interview questions", "is_active": True, "channels": []},
            {"name": "Answering with the STAR Method", "strategy": "TOPIC_CURATED", "search_query": "STAR method interview", "is_active": True, "channels": ["Jeff H Sipe", "Dan Croitor", "A Life After Layoff", "Linda Raynier"]},
            {"name": "Teamwork & Conflict", "strategy": "TOPIC_CURATED", "search_query": "behavioral interview teamwork conflict", "is_active": True, "channels": ["Jeff H Sipe", "Dan Croitor", "A Life After Layoff", "Linda Raynier"]},
            {"name": "Amazon's Leadership Principles", "strategy": "TOPIC_CURATED", "search_query": "'amazon leadership principles' interview", "is_active": True, "channels": ["Jeff H Sipe", "Dan Croitor"]},
            {"name": "Google's 'Googliness'", "strategy": "TOPIC_CURATED", "search_query": "google 'googliness' interview", "is_active": True, "channels": ["Exponent", "Dan Croitor"]},
        ]
    },
    {
        "main_category": "dev_productivity",
        "subcategories": [
            {"name": "Most Watched", "strategy": "POPULARITY", "search_query": "developer productivity", "is_active": True, "channels": []},
            {"name": "Git & Version Control", "strategy": "TOPIC_CURATED", "search_query": "git tutorial advanced", "is_active": True, "channels": ["Fireship", "freeCodeCamp.org", "ThePrimeTime", "GitKraken"]},
            {"name": "Docker & Containers", "strategy": "TOPIC_CURATED", "search_query": "docker tutorial", "is_active": True, "channels": ["Fireship", "freeCodeCamp.org", "Tech With Tim", "Hussein Nasser", "Docker", "Jeff Geerling"]},
            {"name": "VS Code Tips & Tricks", "strategy": "TOPIC_CURATED", "search_query": "'vs code' tips tricks", "is_active": True, "channels": ["Fireship", "ThePrimeTime", "Theo - t3.gg", "James Q Quick"]},
        ]
    },
    {
        "main_category": "ai_ml",
        "subcategories": [
            {"name": "Most Watched", "strategy": "POPULARITY", "search_query": "machine learning introduction", "is_active": True, "channels": []},
            {"name": "AI & ML Fundamentals", "strategy": "TOPIC_CURATED", "search_query": "machine learning fundamentals", "is_active": True, "channels": ["StatQuest with Josh Starmer", "Two Minute Papers", "Sentdex"]},
            {"name": "Large Language Models (LLMs)", "strategy": "TOPIC_CURATED", "search_query": "large language models explained OR LLM", "is_active": True, "channels": ["Two Minute Papers", "Andrej Karpathy", "Yannic Kilcher", "Lex Fridman"]},
            {"name": "Prompt Engineering", "strategy": "TOPIC_CURATED", "search_query": "prompt engineering tutorial", "is_active": True, "channels": ["Two Minute Papers", "freeCodeCamp.org", "Sentdex"]},
            {"name": "LangChain", "strategy": "TOPIC_CURATED", "search_query": "langchain tutorial", "is_active": True, "channels": ["freeCodeCamp.org", "Sentdex", "Tech With Tim"]},
            {"name": "LangGraph", "strategy": "TOPIC_CURATED", "search_query": "langgraph tutorial", "is_active": True, "channels": ["LangChain", "Sentdex"]},
        ]
    },
    {
        "main_category": "language_python",
        "subcategories": [
            {"name": "Python - Most Watched", "strategy": "POPULARITY", "search_query": "python programming tutorial", "is_active": True, "channels": []},
            {"name": "Python - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "python", "is_active": True, "channels": ["Corey Schafer", "freeCodeCamp.org", "Programming with Mosh", "Tech With Tim"]},
            {"name": "Python - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "python tutorial", "is_active": True, "channels": []},
            {"name": "Python - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "python 'full course' OR masterclass", "is_active": True, "channels": []},
        ]
    },
    {
        "main_category": "language_javascript",
        "subcategories": [
            {"name": "JavaScript - Most Watched", "strategy": "POPULARITY", "search_query": "javascript tutorial OR typescript tutorial", "is_active": True, "channels": []},
            {"name": "JavaScript - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "javascript OR typescript", "is_active": True, "channels": ["Fireship", "The Net Ninja", "Traversy Media", "Jack Herrington"]},
            {"name": "JavaScript - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "javascript concepts OR typescript concepts", "is_active": True, "channels": []},
            {"name": "JavaScript - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "javascript 'full course' OR typescript masterclass", "is_active": True, "channels": []},
        ]
    },
    {
        "main_category": "language_java",
        "subcategories": [
            {"name": "Java - Most Watched", "strategy": "POPULARITY", "search_query": "java programming tutorial", "is_active": True, "channels": []},
            {"name": "Java - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "java", "is_active": True, "channels": ["Amigoscode", "Bro Code", "Telusko", "freeCodeCamp.org"]},
            {"name": "Java - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "java concepts", "is_active": True, "channels": []},
            {"name": "Java - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "java 'full course' OR masterclass", "is_active": True, "channels": []},
        ]
    },
    {
        "main_category": "language_cpp",
        "subcategories": [
            {"name": "C++ - Most Watched", "strategy": "POPULARITY", "search_query": "c++ programming tutorial", "is_active": True, "channels": []},
            {"name": "C++ - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "c++", "is_active": True, "channels": ["The Cherno", "CodeBeauty", "Jason Turner", "freeCodeCamp.org"]},
            {"name": "C++ - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "c++ concepts", "is_active": True, "channels": []},
            {"name": "C++ - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "c++ 'full course' OR masterclass", "is_active": True, "channels": []},
        ]
    },
    {
        "main_category": "language_csharp",
        "subcategories": [
            {"name": "C# - Most Watched", "strategy": "POPULARITY", "search_query": "c# programming tutorial", "is_active": True, "channels": []},
            {"name": "C# - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "c#", "is_active": True, "channels": ["IAmTimCorey", "Nick Chapsas", "Programming with Mosh", "freeCodeCamp.org"]},
            {"name": "C# - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "c# concepts", "is_active": True, "channels": []},
            {"name": "C# - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "c# 'full course' OR masterclass", "is_active": True, "channels": []},
        ]
    },
    {
        "main_category": "language_go",
        "subcategories": [
            {"name": "Go - Most Watched", "strategy": "POPULARITY", "search_query": "golang tutorial", "is_active": True, "channels": []},
            {"name": "Go - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "golang", "is_active": True, "channels": ["Nic Jackson", "JustForFunc", "Anthony GG", "Learn To Code"]},
            {"name": "Go - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "golang concepts", "is_active": True, "channels": []},
            {"name": "Go - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "golang 'full course' OR masterclass", "is_active": True, "channels": []},
        ]
    },
    {
        "main_category": "language_rust",
        "subcategories": [
            {"name": "Rust - Most Watched", "strategy": "POPULARITY", "search_query": "rust programming tutorial", "is_active": True, "channels": []},
            {"name": "Rust - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "rust", "is_active": True, "channels": ["Let's Get Rusty", "No Boilerplate", "Ryan Levick", "freeCodeCamp.org"]},
            {"name": "Rust - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "rust concepts", "is_active": True, "channels": []},
            {"name": "Rust - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "rust 'full course' OR masterclass", "is_active": True, "channels": []},
        ]
    },
    {
        "main_category": "language_sql",
        "subcategories": [
            {"name": "SQL - Most Watched", "strategy": "POPULARITY", "search_query": "sql tutorial for beginners", "is_active": True, "channels": []},
            {"name": "SQL - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "sql", "is_active": True, "channels": ["Alex The Analyst", "kudvenkat", "Programming with Mosh", "freeCodeCamp.org"]},
            {"name": "SQL - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "sql concepts", "is_active": True, "channels": []},
            {"name": "SQL - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "sql 'full course' OR masterclass", "is_active": True, "channels": []},
        ]
    },
    {
        "main_category": "language_kotlin",
        "subcategories": [
            {"name": "Kotlin - Most Watched", "strategy": "POPULARITY", "search_query": "kotlin tutorial", "is_active": True, "channels": []},
            {"name": "Kotlin - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "kotlin", "is_active": True, "channels": ["Philipp Lackner", "CodingWithMitch", "freeCodeCamp.org", "JetBrains TV"]},
            {"name": "Kotlin - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "kotlin concepts", "is_active": True, "channels": []},
            {"name": "Kotlin - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "kotlin 'full course' OR masterclass", "is_active": True, "channels": []},
        ]
    },
    {
        "main_category": "language_swift",
        "subcategories": [
            {"name": "Swift - Most Watched", "strategy": "POPULARITY", "search_query": "swift programming tutorial", "is_active": True, "channels": []},
            {"name": "Swift - Latest Uploads", "strategy": "RECENCY_CURATED", "search_query": "swift", "is_active": True, "channels": ["CodeWithChris", "Sean Allen", "LetsBuildThatApp", "Paul Hudson"]},
            {"name": "Swift - Quick Concepts", "strategy": "FORMAT_DURATION", "search_query": "swift concepts", "is_active": True, "channels": []},
            {"name": "Swift - Masterclasses", "strategy": "FORMAT_KEYWORD", "search_query": "swift 'full course' OR masterclass", "is_active": True, "channels": []},
        ]
    },
]