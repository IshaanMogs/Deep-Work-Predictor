---
inclusion: always
---

# Development Guidelines

## Code Standards
- Use Python 3.9+ for all components
- Follow PEP 8 style guidelines
- Include docstrings for all functions and classes
- Keep functions focused and under 50 lines when possible

## AWS Best Practices
- Use IAM roles with least privilege access
- Store credentials in AWS Secrets Manager or environment variables
- Tag all AWS resources with project identifier: `deep-work-predictor`
- Use SageMaker managed endpoints for cost efficiency

## SageMaker Workflow
- Store training data in S3 with versioning enabled
- Use SageMaker experiments to track model iterations
- Implement model monitoring for drift detection
- Save model artifacts with metadata (hyperparameters, metrics)

## Bedrock Integration
- Use boto3 for Bedrock API calls
- Implement retry logic with exponential backoff
- Cache roadmap templates to reduce API costs
- Structure prompts for consistent, actionable output

## Testing Approach
- Unit tests for data preprocessing functions
- Integration tests for SageMaker training jobs
- End-to-end tests for prediction pipeline
- Mock Bedrock calls in tests to avoid costs

## Deployment
- Use SageMaker model registry for version control
- Implement blue-green deployment for zero downtime
- Set up CloudWatch alarms for endpoint health
- Document rollback procedures
