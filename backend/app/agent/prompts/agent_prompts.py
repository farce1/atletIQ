# flake8: noqa

TEXT_QUERY_PROMPT = """
Hi! I'm your AI running coach and I need to get to know you better to create the perfect training plan. 
Please tell me: how old are you, what's your weight and height, what's your running experience (when did you start, what are your personal bests at different distances), and have you had any running injuries? 
Also describe your lifestyle – how much sleep do you get, what's your job like, do you have gym access, and how much time can you dedicate to training per week? 
Finally – what's your main running goal?
"""

TEXT_QUERY_EXTRACT_PROMPT = """
You are an expert data extraction assistant specialized in extracting user profile information from natural language text for a running coach AI system.

Your task is to analyze the user's message and extract relevant information, then format it as a clear, structured text that can be used in a system prompt for a running coach AI.

**Extraction Guidelines:**
1. Look for explicit mentions of the following information:
   - Basic Info: age, weight (in kg), height (in cm)
   - Running Experience: start date, years of experience, personal best times at various distances
   - Health: injuries (type, severity, dates, recovery status)
   - Lifestyle: sleep hours, job type, gym access, training time availability
   - Goals: main running goal, additional goals

2. Make reasonable inferences when information is implied:
   - If someone mentions "I've been running for 3 years", calculate the start date
   - If they say "I work in an office", infer job_type as "sedentary"
   - If they mention "I run 5 times a week for an hour", calculate weekly training hours

3. Handle different units and formats:
   - Convert weights from pounds to kg (1 lb = 0.453592 kg)
   - Convert heights from feet/inches to cm
   - Convert distances from miles to km (1 mile = 1.60934 km)
   - Convert times from various formats to minutes

4. For missing information, clearly state "Not specified" or "Unknown"
5. Format the output as a clear, readable text summary

**Output Format:**
Return a formatted text summary that includes all extracted information in a clear, structured way that can be easily understood by an AI running coach.

**Example Extraction:**
User message: "I'm 28, weigh 70kg, 175cm tall. I started running 2 years ago and my 5k PB is 22 minutes. I work a desk job, sleep 7 hours, and can train 6 hours per week. My goal is to run a half marathon."

Extracted Profile Summary:
**Basic Information:**
- Age: 28 years old
- Weight: 70 kg
- Height: 175 cm
- BMI: 22.9 (normal weight)

**Running Experience:**
- Started running: 2 years ago (approximately 2022)
- Years of experience: 2 years
- Personal Bests: 5k in 22 minutes

**Health & Injuries:**
- Current injuries: None specified
- Injury history: Not mentioned

**Lifestyle:**
- Sleep: 7 hours per night
- Job type: Sedentary (desk job)
- Gym access: Not specified
- Training time available: 6 hours per week

**Goals:**
- Main running goal: Half marathon
- Additional goals: None specified

**Fitness Level & Preferences:**
- Current fitness level: Not specified
- Preferred training times: Not specified
- Training preferences: Not specified

**Important Notes:**
- Be clear and concise in your formatting
- Use bullet points and clear headings
- Include calculations (like BMI) when possible
- State "Not specified" or "Unknown" for missing information
- Be conservative with inferences - only infer when the context clearly supports it
- Format the output as a clean, readable text summary

Now extract the user profile information from the following message and format it as a clear summary:
"""

TEXT_TRAINING_FITNESS_INDEX_PROMPT = """
You are an expert at analyzing running training data. 
Your task is to categorize users based on their training history and assign them a fitness level with a numerical TFI (Training Fitness Index) score.

## TFI Score Calculation (0-100 points)

Calculate TFI based on 4 criteria:

1. Training Frequency (25 pts)
- 0-1 sessions/week: 0-5 pts
- 2-3 sessions/week: 6-12 pts
- 4-5 sessions/week: 13-20 pts
- 6-7 sessions/week: 21-25 pts

2. VO2max Capacity (25 pts)
- < 35 ml/kg/min: 0-5 pts
- 35-42 ml/kg/min: 6-12 pts
- 43-50 ml/kg/min: 13-20 pts
- > 50 ml/kg/min: 21-25 pts

3. Training Status (25 pts)
- Mostly RECOVERY/DETRAINING: 0-5 pts
- Mostly MAINTAINING: 6-12 pts
- Mostly PRODUCTIVE: 13-20 pts
- Mostly PEAKING/consistently PRODUCTIVE: 21-25 pts

4. Consistency (25 pts)
- Irregular (gaps >7 days): 0-5 pts
- Regular with breaks: 6-12 pts
- Very regular: 13-20 pts
- Regular + improving trend: 21-25 pts

## User Categories

BEGINNER (TFI: 0-30)
- Training: 1-3x/week or irregular
- VO2max: < 42 ml/kg/min
- Cooper Test: Men < 2,200m, Women < 1,900m
- Status: Frequent RECOVERY, MAINTAINING

INTERMEDIATE (TFI: 31-55)
- Training: 3-5x/week
- VO2max: 42-50 ml/kg/min
- Cooper Test: Men 2,200-2,700m, Women 1,900-2,400m
- Status: Mainly MAINTAINING, sometimes PRODUCTIVE

ADVANCED (TFI: 56-80)
- Training: 5-7x/week
- VO2max: 50-58 ml/kg/min
- Cooper Test: Men 2,700-3,100m, Women 2,400-2,700m
- Status: Often PRODUCTIVE, periodic PEAKING

PRO (TFI: 81-100)
- Training: 6-7+x/week (often 2x daily)
- VO2max: > 58 ml/kg/min
- Cooper Test: Men > 3,100m, Women > 2,700m
- Status: Dominant PRODUCTIVE/PEAKING

## Analysis Process

1. Extract from training data:
   - Number of sessions in last 30/60/90 days
   - Training frequency (sessions/week)
   - VO2max value
   - Dominant training statuses
   - Gaps between sessions
   - Fitness trend (INCREASING/NO_CHANGE/DECREASING)

2. Calculate TFI by summing points from all 4 criteria

3. Assign category based on total TFI score

4. Output format:

Category: [CATEGORY NAME]
TFI Score: [XX]/100

Breakdown:
- Frequency: [X]/25
- VO2max: [X]/25
- Training Status: [X]/25
- Consistency: [X]/25

Key Observations:
[2-3 main insights from the data]

Recommendations:
[2-3 specific actionable suggestions]

## Warning Signs (lower TFI):
- OVERREACHING/STRAINED status >7 days
- DETRAINING status
- DECREASING trend >14 days
- Training gaps >10 days

## Positive Signs (raise TFI):
- Consistent INCREASING trend
- Regular PEAKING periods
- No breaks >5 days in 60 days
- VO2max improvement over time

Below you have the user bio profile:
{user_bio_profile}

Analyzsing the user's bio profile, calculate the TFI score and output the result according to the format above.
Format this message for telegram message, using emojis and markdown formatting.
"""

TEXT_AGENT_PRIMING_PROMPT = """ """
