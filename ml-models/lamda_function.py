import json
import boto3
import time
import re

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb").Table("UserProductivityTable")


def lambda_handler(event, context):

    # -----------------------------
    # Parse API Gateway request
    # -----------------------------
    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    user_id = body.get("user_id", "student_19")
    user_goal = body.get("goal", "Master DSA")
    vitals = body.get("vitals", [7, 30, 3, 45])

    sleep, exercise, stress, noise = vitals

    # -----------------------------
    # Focus score model
    # -----------------------------
    raw_score = (sleep * 7) + (exercise * 0.3) - (stress * 4) - (noise * 0.2) + 40
    focus_score = max(0, min(100, round(raw_score)))

    decision = "FOCUS NOW" if focus_score > 70 and stress < 6 else "RECOVERY REQUIRED"

    # -----------------------------
    # Cognitive state detection
    # -----------------------------
    if focus_score >= 85 and stress <= 4:
        state = "DEEP_WORK_OPTIMAL"

    elif focus_score >= 70 and stress <= 6:
        state = "FOCUSED_LEARNING"

    elif focus_score >= 50:
        state = "LIGHT_LEARNING"

    else:
        state = "RECOVERY_MODE"

    # -----------------------------
    # Strategy engine
    # -----------------------------
    if state == "DEEP_WORK_OPTIMAL":
        strategy = "hard problem solving and algorithm implementation"

    elif state == "FOCUSED_LEARNING":
        strategy = "guided practice with medium difficulty problems"

    elif state == "LIGHT_LEARNING":
        strategy = "concept reinforcement and small exercises"

    else:
        strategy = "recovery routine and light review"

    # -----------------------------
    # LLM Prompt
    # -----------------------------
    prompt_text = f"""
You are a productivity planning engine.

User Goal: {user_goal}
Focus Score: {focus_score}/100

Generate EXACTLY 3 deep work steps.

STRICT RULES:
- Return ONLY the steps
- Do NOT write explanations
- Do NOT write code
- Do NOT add extra text
- Do NOT repeat steps
- Do NOT generate more than 3 steps

FORMAT STRICTLY:

Step 1
Time Block: <minutes>
Action: <specific study action>
Output: <measurable outcome>

Step 2
Time Block: <minutes>
Action: <specific study action>
Output: <measurable outcome>

Step 3
Time Block: <minutes>
Action: <specific study action>
Output: <measurable outcome>
"""

    # -----------------------------
    # Call Bedrock
    # -----------------------------
    try:

        response = bedrock.converse(
            modelId="meta.llama3-70b-instruct-v1:0",
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt_text}]
                }
            ],
            inferenceConfig={
                "maxTokens": 200,
                "temperature": 0.3,
                "topP": 0.9
            }
        )

        roadmap_raw = response["output"]["message"]["content"][0]["text"]

        # -----------------------------
        # Extract only steps
        # -----------------------------
        steps = re.findall(
            r"Step\s*\d+\s*[\s\S]*?(?=Step\s*\d+|$)",
            roadmap_raw
        )

        steps = steps[:3]

        clean_steps = []

        for i, step in enumerate(steps):
            step = re.sub(r"Step\s*\d+", f"Step {i+1}", step)
            clean_steps.append(step.strip())

        roadmap = "\n\n".join(clean_steps)

    except Exception as e:

        roadmap = f"""Step 1
Time Block: 30 minutes
Action: Review fundamentals of {user_goal}
Output: Clear understanding of key concepts

Step 2
Time Block: 30 minutes
Action: Practice medium difficulty problems
Output: Solve 3 practice questions

Step 3
Time Block: 30 minutes
Action: Review mistakes and summarize learnings
Output: Written notes of key insights
"""

    # -----------------------------
    # Save session to DynamoDB
    # -----------------------------
    timestamp = int(time.time())

    dynamodb.put_item(
        Item={
            "user_id": user_id,
            "timestamp": timestamp,
            "vitals": vitals,
            "focus_score": focus_score,
            "cognitive_state": state,
            "goal": user_goal,
            "decision": decision,
            "strategy": strategy,
            "roadmap": roadmap
        }
    )

    # -----------------------------
    # Return API response
    # -----------------------------
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "user_id": user_id,
            "focus_score": focus_score,
            "decision": decision,
            "cognitive_state": state,
            "strategy": strategy,
            "personalized_roadmap": roadmap,
            "db_status": "Saved Successfully"
        })
    }
