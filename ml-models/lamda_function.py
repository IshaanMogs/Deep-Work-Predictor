import json
import boto3
import time

def lambda_handler(event, context):
    # Initialize AWS Clients
    bedrock = boto3.client(service_name='bedrock-runtime')
    dynamodb = boto3.resource('dynamodb').Table('UserProductivityTable')
    
    # Get Inputs (from UI or Test Event)
    user_id = event.get('user_id', 'student_19')
    user_goal = event.get('goal', 'Master DSA Recursion')
    # Vitals: [sleep, exercise, stress, noise]
    vitals = event.get('vitals', [7, 30, 3, 45]) 
    
    # Calculate Focus Score (Linear Regression Logic)
    raw_score = (vitals[0] * 7) + (vitals[1] * 0.3) - (vitals[2] * 4) - (vitals[3] * 0.2) + 40
    focus_score = max(0, min(100, round(raw_score)))
    
    # Logistic Decision (Action Logic)
    # Binary Classification: Focus Now (1) or Recover (0)
    status = "FOCUS NOW" if focus_score > 70 and vitals[2] < 6 else "RECOVERY REQUIRED"
    
    # Generate GenAI Roadmap (Amazon Bedrock - Claude 3.5 Sonnet)
    prompt_text = f"Human: User Goal: {user_goal}. Focus Score: {focus_score}/100. Status: {status}. Provide a 3-step deep work roadmap based on this. Assistant:"
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]
    })

    try:
        response = bedrock.invoke_model(
            body=body,
            modelId='anthropic.claude-3-5-sonnet-20240620-v1:0'
        )
        response_body = json.loads(response.get('body').read())
        roadmap = response_body['content'][0]['text']
    except Exception as e:
        roadmap = f"Focus on {user_goal} for 90 minutes. (AI Roadmap error: {str(e)})"

    # Save to DynamoDB (Persistence)
    timestamp = int(time.time())
    dynamodb.put_item(Item={
        'user_id': user_id,
        'timestamp': timestamp,
        'focus_score': focus_score,
        'goal': user_goal,
        'status': status,
        'roadmap': roadmap
    })

    return {
        'statusCode': 200,
        'body': {
            'user_id': user_id,
            'focus_score': focus_score,
            'decision': status,
            'personalized_roadmap': roadmap,
            'db_status': 'Saved Successfully'
        }
    }
