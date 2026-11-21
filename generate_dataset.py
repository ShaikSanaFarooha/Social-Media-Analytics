"""
Dataset Generator for Social Media Analytics Project
Generates 225+ realistic social media posts with positive, negative, and neutral sentiments.
"""

import csv
import os
import random
from datetime import datetime, timedelta

# Create data directory if not exists
os.makedirs("data", exist_ok=True)

# List of realistic user handles
USERS = [
    "alex_dev", "data_diva", "tech_guru", "code_ninja", "cyber_sam",
    "ai_explorer", "sarah_codes", "david_analyst", "priya_tech", "cloud_charlie",
    "rachel_data", "vikram_ml", "emma_designs", "kevin_builds", "sophia_ai",
    "rahul_coder", "zoe_analytics", "marcus_bytes", "lisa_cloud", "arjun_python",
    "elena_trends", "chris_flutter", "neha_insights", "daniel_ops", "maya_stats"
]

PLATFORMS = ["X (Twitter)", "Instagram", "Facebook"]

# Structured realistic posts with inherent sentiment and matching hashtags
POST_TEMPLATES = [
    # POSITIVE POSTS (Tech, AI, Success, Excitement, Learning)
    ("Just completed my first Deep Learning project with 98% accuracy! Absolutely thrilled with the results.",
     "Positive", "#DeepLearning, #AI, #MachineLearning, #Python", (250, 4200), (30, 450), (15, 300)),
    ("Streamlit makes building machine learning web apps ridiculously fast and beautiful. Loving this framework!",
     "Positive", "#Streamlit, #Python, #WebDev, #DataScience", (300, 3800), (20, 290), (10, 180)),
    ("Super excited to announce that I have joined Google as a Machine Learning Engineer intern! Dream come true.",
     "Positive", "#DreamJob, #TechCareers, #Google, #Internship", (800, 5200), (90, 850), (45, 620)),
    ("The new generative AI update from OpenAI is mind-blowing. The latency is almost zero and reasoning is phenomenal.",
     "Positive", "#GenerativeAI, #OpenAI, #Innovation, #FutureTech", (400, 4500), (50, 520), (25, 390)),
    ("Python remains the undisputed king for Big Data analytics and data manipulation. Pandas 2.0 is incredible!",
     "Positive", "#Python, #Pandas, #BigData, #DataAnalytics", (180, 2900), (15, 210), (8, 140)),
    ("Had an amazing mentoring session today with aspiring computer science students. Their passion for coding is inspiring!",
     "Positive", "#Mentorship, #BTech, #Coding, #StudentLife", (120, 1800), (18, 160), (6, 95)),
    ("Proud to share our research paper on Sentiment Analysis using Transformer models got accepted at IEEE!",
     "Positive", "#Research, #NLP, #IEEE, #AI", (450, 3900), (60, 480), (30, 320)),
    ("Big thanks to the open-source community! Without scikit-learn and PyTorch, our startup wouldn't exist.",
     "Positive", "#OpenSource, #PyTorch, #ScikitLearn, #Startups", (210, 2400), (22, 190), (12, 150)),
    ("Morning coffee, dual monitors, and clean bug-free code. The perfect start to a productive Saturday!",
     "Positive", "#DeveloperLife, #Productivity, #Coding, #Coffee", (160, 2100), (14, 130), (5, 75)),
    ("Just finished reading 'Designing Data-Intensive Applications'. Easily the best engineering book I have ever read.",
     "Positive", "#BigData, #SystemDesign, #SoftwareEngineering, #Books", (320, 3400), (40, 310), (18, 240)),
    ("Finally deployed our college mini-project on Cloud! Clean UI and real-time analytics working flawlessly.",
     "Positive", "#ProjectDeployment, #CloudComputing, #BTech, #Streamlit", (190, 2600), (25, 220), (14, 160)),
    ("Data visualization with Plotly is pure magic! Interactive dashboards make insights pop so elegantly.",
     "Positive", "#Plotly, #DataViz, #DataScience, #Analytics", (140, 1950), (16, 175), (9, 110)),
    ("Gratitude post: Reached 10,000 followers on tech tips! Thank you all for supporting my developer journey.",
     "Positive", "#Milestone, #TechCommunity, #Gratitude, #Growth", (500, 4800), (75, 620), (35, 410)),
    ("Our university hackathon was an absolute blast! Huge congratulations to all the creative innovators.",
     "Positive", "#Hackathon, #Innovation, #StudentLife, #Engineering", (220, 2800), (32, 280), (19, 190)),
    ("Cloud certifications really boosted my career prospects. Excited for the new cloud computing adventures ahead!",
     "Positive", "#CloudComputing, #AWS, #TechCareers, #Certifications", (280, 3100), (35, 305), (15, 210)),
    ("Automated our team's entire data processing pipeline using Python scripts. Saved 15 hours of manual work weekly!",
     "Positive", "#Python, #Automation, #BigData, #Productivity", (310, 3600), (42, 340), (22, 260)),
    ("Received wonderful feedback from the professor on our Big Data Analytics project. Hard work truly pays off!",
     "Positive", "#CollegeProjects, #BigData, #AcademicSuccess, #AI", (175, 2300), (20, 190), (10, 130)),
    ("Loving the new dark mode and terminal integration in VS Code. It just keeps getting better and smoother.",
     "Positive", "#VSCode, #DeveloperTools, #Programming, #Productivity", (260, 3300), (28, 270), (16, 185)),
    ("Nature walk after a marathon coding week is the best mental reset ever. Highly recommend taking breaks!",
     "Positive", "#MentalHealth, #WorkLifeBalance, #Nature, #Wellness", (130, 1700), (12, 140), (4, 60)),
    ("Collaborating with such a talented data engineering squad is an absolute joy. Great team culture matters!",
     "Positive", "#Teamwork, #DataEngineering, #TechCulture, #Leadership", (210, 2500), (24, 210), (11, 145)),

    # NEGATIVE POSTS (Complaints, Frustration, Bugs, Server Down, Outages, Criticisms)
    ("Another cloud service outage in the middle of our client demo! Completely unacceptable reliability from this vendor.",
     "Negative", "#CloudOutage, #Downtime, #ServerDown, #Frustration", (95, 1450), (45, 380), (28, 250)),
    ("Why is customer service so terrible these days? Waited 45 minutes on call and got disconnected without answers.",
     "Negative", "#CustomerService, #TerribleExperience, #WorstSupport", (120, 1900), (55, 420), (35, 310)),
    ("Spent 6 hours debugging only to realize a missing comma in the JSON config file. Coding can be agonizing sometimes.",
     "Negative", "#CodingStruggles, #Debugging, #DeveloperProblems, #BugLife", (180, 2600), (38, 310), (18, 170)),
    ("The latest mobile app update broke the user interface and caused immediate battery drain. Horrible release!",
     "Negative", "#AppUpdate, #Buggy, #PoorQuality, #BadUpdate", (140, 2200), (62, 510), (40, 360)),
    ("Cybersecurity breaches are getting totally out of control. When will organizations take data privacy seriously?",
     "Negative", "#CyberSecurity, #DataBreach, #PrivacyFail, #Infosec", (210, 2900), (48, 410), (30, 280)),
    ("Extremely disappointed with this laptop's thermal throttling. Fans sound like a jet engine during basic data processing.",
     "Negative", "#HardwareFail, #TechReview, #Overheating, #Disappointed", (110, 1600), (34, 280), (16, 140)),
    ("Internet service has been down since morning right when university exams are ongoing. Worst ISP ever!",
     "Negative", "#InternetDown, #StudentLife, #ISPfail, #NoConnection", (135, 1850), (42, 360), (25, 230)),
    ("Hate when recruiters send automated rejection emails after 4 rounds of grueling technical interviews. So disrespectful.",
     "Negative", "#JobSearch, #Recruitment, #HiringFail, #TechJobs", (320, 3800), (85, 710), (50, 480)),
    ("Misleading advertisements everywhere! The AI tool barely does 10% of what was promised on the landing page.",
     "Negative", "#FalseAdvertising, #AIHype, #Disappointed, #TechScam", (170, 2400), (50, 430), (28, 260)),
    ("The social media algorithm is utterly ruined. Genuine content gets zero reach while clickbait gets millions of views.",
     "Negative", "#SocialMediaAlgorithms, #BadReach, #Frustrated, #ContentCreator", (280, 3400), (70, 600), (42, 390)),
    ("Package arrived two weeks late and the item inside was damaged. Horrible logistics service!",
     "Negative", "#DeliveryDelay, #DamagedItem, #BadService, #UnhappyCustomer", (90, 1300), (30, 250), (14, 120)),
    ("Flight got delayed by 7 hours with no explanation or food vouchers offered. Disastrous airline management.",
     "Negative", "#TravelNightmare, #FlightDelayed, #PoorService, #AirlineReview", (160, 2300), (44, 380), (26, 240)),
    ("GPU prices are still ridiculous. Building a budget machine learning workstation is impossible right now.",
     "Negative", "#GPU, #HardwarePrices, #TechBudget, #MachineLearning", (230, 3100), (52, 450), (31, 290)),
    ("Dealing with spaghetti legacy code with zero documentation. What a painful headache of a work day.",
     "Negative", "#LegacyCode, #TechDebt, #BadPractices, #DeveloperPain", (150, 2100), (36, 300), (18, 160)),
    ("The API rate limits on the new platform are ridiculously strict. Breaks our production data analytics pipelines.",
     "Negative", "#APILimits, #DevRant, #BigData, #DataPipelines", (115, 1750), (28, 240), (15, 130)),
    ("Constant popups and intrusive ads make browsing modern websites an absolute nightmare. Unusable web design.",
     "Negative", "#WebDesign, #BadUX, #AdOverload, #Frustration", (190, 2700), (46, 390), (24, 220)),
    ("Cloud bill arrived and it is 3x higher than estimated due to confusing hidden egress charges. What a rip-off!",
     "Negative", "#CloudCosts, #AWSBill, #HiddenFees, #FinOps", (260, 3500), (64, 530), (38, 350)),

    # NEUTRAL POSTS (Announcements, Tutorials, News, Inquiries, Informational)
    ("Python 3.13 is now officially available with performance improvements and experimental free-threading mode.",
     "Neutral", "#Python, #TechNews, #Programming, #Release", (180, 2700), (25, 230), (20, 210)),
    ("Here is a quick comparison between TextBlob and VADER for social media sentiment classification pipelines.",
     "Neutral", "#NLP, #DataScience, #SentimentAnalysis, #TextBlob", (140, 2200), (18, 180), (15, 160)),
    ("What are your favorite data visualization libraries in Python? Matplotlib, Seaborn, or Plotly?",
     "Neutral", "#Python, #DataViz, #Poll, #CodingCommunity", (160, 2400), (45, 390), (12, 120)),
    ("The global conference on Big Data and Artificial Intelligence scheduled for November 2026 registration is open.",
     "Neutral", "#BigDataConference, #AI, #TechEvents, #Registration", (120, 1900), (14, 140), (10, 110)),
    ("Step-by-step tutorial: How to load, clean, and visualize large CSV datasets using Pandas and Streamlit.",
     "Neutral", "#Tutorial, #Pandas, #Streamlit, #DataAnalytics", (210, 2900), (26, 240), (22, 230)),
    ("Survey results show 68% of computer science students prefer Python for their college mini projects.",
     "Neutral", "#BTech, #Survey, #Python, #StudentStats", (150, 2300), (20, 200), (16, 170)),
    ("Understanding time complexity: Why Big O notation matters in technical coding interviews.",
     "Neutral", "#Algorithms, #DataStructures, #ComputerScience, #Coding", (230, 3100), (28, 260), (24, 250)),
    ("Microsoft releases new security advisory regarding zero-day vulnerability in web servers.",
     "Neutral", "#CyberSecurity, #TechNews, #SecurityAdvisory, #Infosec", (170, 2500), (22, 210), (18, 190)),
    ("Checking out the differences between SQL and NoSQL databases for high-velocity social media streaming data.",
     "Neutral", "#Databases, #SQL, #NoSQL, #BigData", (190, 2600), (24, 220), (19, 200)),
    ("Live webinar today at 5 PM on Natural Language Processing architectures and sentiment evaluation methods.",
     "Neutral", "#Webinar, #NLP, #DataScience, #FreeLearning", (130, 1800), (15, 150), (11, 120)),
    ("How do you handle missing values and null entries in your exploratory data analysis workflow?",
     "Neutral", "#DataAnalysis, #Pandas, #DataCleaning, #Discussion", (145, 2100), (38, 320), (10, 110)),
    ("Latest report indicates global Big Data analytics market size projected to reach $655 billion by 2030.",
     "Neutral", "#BigData, #MarketResearch, #IndustryTrends, #Analytics", (240, 3200), (30, 270), (25, 260)),
    ("Comparing AWS, Azure, and Google Cloud Platform for hosting containerized microservices and web apps.",
     "Neutral", "#CloudComputing, #AWS, #Azure, #GCP", (200, 2800), (27, 250), (21, 220)),
    ("New research article explains the mathematical intuition behind backpropagation in neural networks.",
     "Neutral", "#Mathematics, #NeuralNetworks, #DeepLearning, #AI", (165, 2400), (19, 190), (17, 180)),
    ("Overview of popular data preprocessing techniques: One-hot encoding, min-max scaling, and standardization.",
     "Neutral", "#DataScience, #MachineLearning, #DataPreprocessing, #Python", (175, 2500), (23, 210), (18, 190))
]

# Additional content variations to reach 225+ distinct posts
VARIATIONS = [
    # Positive variations
    ("Loved attending the national level AI symposium today! Met so many brilliant researchers and developers.",
     "Positive", "#AI, #Conference, #Networking, #Innovation", (190, 2700), (25, 230), (14, 150)),
    ("Just hit a new personal record in the gym: 100kg deadlift! Consistency is key.",
     "Positive", "#FitnessGoals, #GymMotivation, #HealthAndWellness, #Strength", (140, 2100), (22, 210), (8, 90)),
    ("Clean code is not written by following a set of rules. Clean code is created by following discipline.",
     "Positive", "#CleanCode, #SoftwareEngineering, #Programming, #BestPractices", (310, 3900), (40, 350), (28, 290)),
    ("Our open source contribution just got merged into the main branch of NumPy! Honored to contribute.",
     "Positive", "#OpenSource, #NumPy, #Python, #Community", (420, 4400), (55, 490), (32, 330)),
    ("Sunset view at the beach after a long productive coding sprint. Truly serene and peaceful.",
     "Positive", "#TravelDiaries, #Sunset, #Peaceful, #Wanderlust", (220, 3100), (18, 170), (10, 110)),
    ("Just deployed our sentiment analysis model with 95% accuracy! Such a satisfying milestone.",
     "Positive", "#SentimentAnalysis, #NLP, #MachineLearning, #Python", (280, 3700), (36, 320), (20, 210)),
    ("Big shoutout to my university professors for guiding us through this Big Data Analytics mini-project.",
     "Positive", "#BTech, #Mentorship, #AcademicSuccess, #BigData", (150, 2200), (19, 180), (11, 120)),
    ("This new coffee shop has high-speed WiFi, quiet ambiance, and the best espresso in town. New coding spot!",
     "Positive", "#CoffeeLover, #RemoteWork, #WorkFromCafe, #Productivity", (110, 1600), (14, 130), (6, 70)),
    ("Our student team won 1st prize in the state-level Hackathon competition! Hard work paid off immensely.",
     "Positive", "#HackathonWinner, #Champions, #StudentLife, #Engineering", (650, 5100), (80, 720), (45, 450)),
    ("Learning data visualization with Plotly and Seaborn has completely transformed how I present findings.",
     "Positive", "#DataViz, #Seaborn, #Plotly, #Analytics", (170, 2400), (21, 200), (12, 130)),

    # Negative variations
    ("Another data pipeline failed overnight because someone altered the database schema without notice. Frustrating!",
     "Negative", "#DataPipelineFail, #TechDebt, #BadPractices, #DeveloperPain", (140, 2100), (36, 310), (19, 170)),
    ("Worst flight experience ever. Luggage misplaced and staff refused to assist properly.",
     "Negative", "#TravelNightmare, #LostLuggage, #PoorCustomerService, #Disappointed", (175, 2500), (48, 420), (27, 260)),
    ("The new user interface on this social media app is confusing, clunky, and bloated. Downgrade!",
     "Negative", "#BadUX, #AppDesign, #UserExperience, #Disappointed", (210, 2900), (52, 460), (31, 290)),
    ("High latency and continuous buffering during the live stream. Terrible CDN performance.",
     "Negative", "#Buffering, #LiveStreamFail, #TechIssues, #Frustrated", (115, 1750), (32, 280), (17, 160)),
    ("Spam emails flooding the inbox despite enabling strict anti-phishing filters. Annoying security loophole.",
     "Negative", "#Spam, #CyberSecurity, #EmailFail, #Annoyed", (125, 1850), (28, 250), (15, 140)),
    ("Tried upgrading the Python virtual environment and now half the dependencies are conflicting. Dependency hell!",
     "Negative", "#Python, #DependencyHell, #PipFail, #DeveloperStruggles", (240, 3200), (45, 390), (25, 240)),
    ("The restaurant charged double for mediocre food and lukewarm drinks. Highly do not recommend.",
     "Negative", "#FoodReview, #PoorService, #BadExperience, #Overpriced", (130, 1900), (34, 300), (18, 170)),
    ("Battery health dropped by 10% in just two months after the latest OS patch. Terrible battery optimization.",
     "Negative", "#BatteryDrain, #OSUpdate, #HardwareIssues, #Unhappy", (180, 2600), (42, 370), (24, 230)),
    ("Job posting requires 10 years of experience for an entry-level position with junior pay. Absurd hiring culture.",
     "Negative", "#JobSearch, #HiringFail, #TechCareers, #Unrealistic", (380, 4500), (90, 800), (55, 520)),
    ("Cloud server crashed right before the final submission deadline. What bad timing!",
     "Negative", "#ServerCrash, #StudentLife, #DeadlineStress, #Panic", (205, 2800), (50, 440), (29, 280)),

    # Neutral variations
    ("Exploring the performance benchmarks between FastAPI and Flask for serving machine learning models.",
     "Neutral", "#FastAPI, #Flask, #Python, #API", (160, 2300), (22, 210), (17, 180)),
    ("Reminder: The college campus placement drive for engineering students begins next Monday at 9 AM.",
     "Neutral", "#CampusPlacement, #BTech, #JobDrive, #Notice", (190, 2700), (28, 260), (20, 210)),
    ("Guide to understanding Confusion Matrix, Precision, Recall, and F1-Score in machine learning evaluation.",
     "Neutral", "#MachineLearning, #Metrics, #DataScience, #Tutorial", (220, 3000), (27, 250), (22, 230)),
    ("Analyzing sentiment classification scores across multiple social media platforms with natural language processing.",
     "Neutral", "#SentimentAnalysis, #BigData, #NLP, #Research", (155, 2250), (20, 190), (16, 170)),
    ("New firmware update 4.2.1 is rolling out today with critical security patches and minor bug fixes.",
     "Neutral", "#FirmwareUpdate, #TechNews, #PatchNotes, #Security", (135, 1950), (16, 160), (12, 130)),
    ("How do you prefer structuring your Python projects? Modular architecture vs single-file scripts?",
     "Neutral", "#Python, #ProjectStructure, #SoftwareEngineering, #Poll", (175, 2500), (40, 360), (14, 140)),
    ("Comparison of Apache Spark and Pandas when processing tabular datasets exceeding 100 gigabytes.",
     "Neutral", "#ApacheSpark, #Pandas, #BigData, #DataEngineering", (250, 3400), (32, 290), (26, 270)),
    ("The university library has extended its operating hours during end-semester examination week.",
     "Neutral", "#UniversityNews, #StudentLife, #LibraryNotice, #Exams", (120, 1800), (15, 140), (9, 100)),
    ("A breakdown of how VADER handles capitalization, exclamation points, and emojis during sentiment scoring.",
     "Neutral", "#VADER, #SentimentAnalysis, #NLP, #TextProcessing", (165, 2400), (23, 220), (18, 190)),
    ("Introduction to Docker containers for data scientists: Reproducible machine learning environments.",
     "Neutral", "#Docker, #DevOps, #DataScience, #Containers", (200, 2800), (25, 240), (21, 220))
]

def generate_dataset(total_records=230):
    all_templates = POST_TEMPLATES + VARIATIONS
    
    # We want a realistic mix: ~45% Positive, ~28% Negative, ~27% Neutral
    positive_pool = [t for t in all_templates if t[1] == "Positive"]
    negative_pool = [t for t in all_templates if t[1] == "Negative"]
    neutral_pool = [t for t in all_templates if t[1] == "Neutral"]

    records = []
    start_date = datetime(2026, 8, 1, 9, 0, 0)
    
    random.seed(42)  # For reproducible realistic data

    for i in range(1, total_records + 1):
        post_id = f"POST_{i:04d}"
        user = random.choice(USERS)
        platform = random.choice(PLATFORMS)
        
        # Determine sentiment pool by weighted distribution
        rand_val = random.random()
        if rand_val < 0.44:
            template = random.choice(positive_pool)
        elif rand_val < 0.72:
            template = random.choice(negative_pool)
        else:
            template = random.choice(neutral_pool)
            
        text, sentiment_type, hashtags, likes_range, comments_range, shares_range = template
        
        # Add slight natural variation to text if duplicate template chosen
        variation_suffixes = [
            "",
            " What are your thoughts on this?",
            " Really interesting to observe.",
            " Check it out and let me know!",
            " Sharing my perspective here.",
            " Hope this helps someone today.",
            " Definitely worth paying attention to.",
            " Any recommendations?",
            " Highly relevant topic right now.",
            " Thoughts?"
        ]
        
        suffix = random.choice(variation_suffixes) if i > len(all_templates) else ""
        post_text = f"{text}{suffix}"
        
        likes = random.randint(likes_range[0], likes_range[1])
        # Comments typically proportional to likes
        comments = random.randint(comments_range[0], comments_range[1])
        # Shares
        shares = random.randint(shares_range[0], shares_range[1])
        
        # Random date spread over ~110 days
        random_days = random.randint(0, 110)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        post_date = (start_date + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)).strftime("%Y-%m-%d %H:%M:%S")
        
        records.append({
            "Post_ID": post_id,
            "Username": user,
            "Platform": platform,
            "Post_Text": post_text,
            "Hashtags": hashtags,
            "Likes": likes,
            "Comments": comments,
            "Shares": shares,
            "Date": post_date
        })

    # Sort records chronologically
    records.sort(key=lambda x: x["Date"])

    # Write to CSV
    output_path = os.path.join("data", "social_media_data.csv")
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["Post_ID", "Username", "Platform", "Post_Text", "Hashtags", "Likes", "Comments", "Shares", "Date"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Successfully generated {len(records)} realistic social media posts in {output_path}")

if __name__ == "__main__":
    generate_dataset(235)

