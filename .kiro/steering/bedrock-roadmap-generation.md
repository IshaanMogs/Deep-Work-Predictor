---
inclusion: fileMatch
fileMatchPattern: "**/api/**,**/*bedrock*.py,**/*roadmap*.py"
---

# Bedrock Roadmap Generation

## Purpose
Generate personalized productivity roadmaps based on deep work potential predictions and user context.

## Bedrock Model Selection
- **Primary**: Claude 3 Sonnet (balance of quality and cost)
- **Fallback**: Claude 3 Haiku (faster, lower cost)
- **Model ID**: `anthropic.claude-3-sonnet-20240229-v1:0`

## Prompt Structure
```python
prompt_template = """
You are a productivity coach analyzing deep work patterns.

User Profile:
- Deep Work Potential Score: {score}
- Key Limiting Factors: {limiting_factors}
- Optimal Time Windows: {optimal_times}
- Current Habits: {habits}

Generate a 7-day actionable roadmap to improve deep work capacity.
Include:
1. Daily focus time blocks (specific times)
2. Environmental optimizations
3. Habit adjustments
4. Progress milestones

Format as structured JSON with daily tasks.
"""
```

## Response Format
```json
{
  "roadmap": {
    "day_1": {
      "focus_blocks": ["9:00-11:00 AM", "2:00-4:00 PM"],
      "actions": ["Reduce morning caffeine", "Use noise-canceling headphones"],
      "milestone": "Complete 2 hours of deep work"
    }
  },
  "weekly_goal": "Increase deep work score by 15 points"
}
```

## API Configuration
```python
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock_client.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "temperature": 0.7,
        "messages": [{"role": "user", "content": prompt}]
    })
)
```

## Error Handling
- Implement retry with exponential backoff (3 attempts)
- Fallback to template-based roadmap if Bedrock fails
- Log all API errors for monitoring
- Set timeout to 30 seconds

## Cost Optimization
- Cache common roadmap patterns
- Batch requests when possible
- Use Haiku model for simple scenarios
- Limit max_tokens to 2000
