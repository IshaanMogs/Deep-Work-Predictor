# Deep-Work Potential Predictor - Requirements Specification

## Project Overview

A machine learning system that predicts deep work potential and generates personalized productivity roadmaps for students and developers participating in the AI for Bharat Hackathon.

## Personas

### Persona 1: Priya - Computer Science Student
- **Age**: 21
- **Background**: Third-year CS student juggling coursework, projects, and exam preparation
- **Goals**: Maximize study efficiency, identify optimal focus times for complex subjects
- **Pain Points**: Struggles with context switching between subjects, inconsistent productivity patterns
- **Usage Pattern**: Checks deep work potential before study sessions, follows weekly roadmaps during exam season
- **Success Metric**: Increase focused study hours from 3 to 5 hours daily

### Persona 2: Arjun - Software Developer
- **Age**: 28
- **Background**: Full-stack developer working remotely with distributed team across time zones
- **Goals**: Protect deep work time for coding, balance meetings with focused development
- **Pain Points**: Frequent interruptions, difficulty maintaining flow state, burnout from overwork
- **Usage Pattern**: Daily morning check for deep work potential, uses roadmap to schedule coding blocks
- **Success Metric**: Complete 2-3 deep work sessions daily, reduce context switches by 40%

## Functional Requirements (EARS Notation)

### Core Prediction Requirements

**FR-1**: WHEN a user submits their current state data, the system SHALL predict their deep work potential score (0-100) using the SageMaker Multiple Linear Regression model.

**FR-2**: WHERE the user provides incomplete input data, the system SHALL apply median imputation for missing numerical features and mode imputation for categorical features.

**FR-3**: WHILE processing prediction requests, the system SHALL normalize input features using StandardScaler before invoking the SageMaker endpoint.

**FR-4**: IF the SageMaker endpoint returns a prediction, the system SHALL classify the score into three categories: Low (0-30), Moderate (31-70), or High (71-100).

**FR-5**: WHEN the prediction latency exceeds 5 seconds, the system SHALL log a performance warning and return a cached prediction if available.

### Roadmap Generation Requirements

**FR-6**: WHEN a deep work potential score is generated, the system SHALL invoke Amazon Bedrock to generate a personalized 7-day productivity roadmap.

**FR-7**: WHERE the user's score is below 50, the Bedrock prompt SHALL emphasize environmental optimizations and habit changes.

**FR-8**: IF the user's score is above 70, the Bedrock prompt SHALL focus on maintaining current conditions and incremental improvements.

**FR-9**: WHEN generating roadmaps, the system SHALL use Amazon Bedrock's Claude 3 Sonnet model with a maximum token limit of 2000.

**FR-10**: WHERE Bedrock API calls fail after 3 retry attempts, the system SHALL fall back to a template-based roadmap generator.

### Data Collection Requirements

**FR-11**: WHEN a user registers, the system SHALL collect baseline data including: sleep hours, exercise frequency, typical work hours, and workspace environment.

**FR-12**: WHILE users interact with the system, the system SHALL track historical deep work scores to identify trends over time.

**FR-13**: IF a user completes a deep work session, the system SHALL prompt them to provide feedback on actual productivity versus predicted potential.

### User Interface Requirements

**FR-14**: WHEN a user views their prediction, the system SHALL display the numerical score, category label, and top 3 limiting factors.

**FR-15**: WHERE a roadmap is generated, the system SHALL present daily tasks in chronological order with specific time blocks.

**FR-16**: IF the user requests historical data, the system SHALL visualize score trends over the past 30 days using a line chart.

**FR-17**: WHEN a user accesses the system on mobile devices, the interface SHALL adapt to screen sizes below 768px width.

### Model Training Requirements

**FR-18**: WHEN training the regression model, the system SHALL use SageMaker Linear Learner with an 80/20 train-test split.

**FR-19**: WHERE model performance metrics are calculated, the system SHALL compute R², RMSE, and MAE on the test set.

**FR-20**: IF the model's R² score falls below 0.7, the system SHALL trigger an alert for model retraining.

**FR-21**: WHILE training, the system SHALL perform 5-fold cross-validation to assess model stability.

## Non-Functional Requirements

### Performance

**NFR-1**: The SageMaker prediction endpoint SHALL respond within 100ms for 95% of requests.

**NFR-2**: The Bedrock roadmap generation SHALL complete within 10 seconds for 99% of requests.

**NFR-3**: The system SHALL support at least 100 concurrent users during hackathon demonstration.

### Reliability

**NFR-4**: The prediction service SHALL maintain 99% uptime during the hackathon evaluation period.

**NFR-5**: All AWS service calls SHALL implement exponential backoff retry logic with a maximum of 3 attempts.

**NFR-6**: The system SHALL gracefully degrade to cached or template-based responses if AWS services are unavailable.

### Security

**NFR-7**: All AWS credentials SHALL be stored in AWS Secrets Manager or environment variables, never in code.

**NFR-8**: User data SHALL be encrypted at rest in S3 using AES-256 encryption.

**NFR-9**: API endpoints SHALL implement rate limiting of 100 requests per user per hour.

**NFR-10**: IAM roles SHALL follow the principle of least privilege for all AWS resource access.

### Scalability

**NFR-11**: The SageMaker endpoint SHALL use auto-scaling with a minimum of 1 and maximum of 5 instances.

**NFR-12**: Training data in S3 SHALL support versioning to enable model rollback.

**NFR-13**: The system architecture SHALL support horizontal scaling for the API layer.

### Usability

**NFR-14**: The prediction interface SHALL require no more than 5 input fields for basic predictions.

**NFR-15**: Roadmap recommendations SHALL use plain language understandable to non-technical users.

**NFR-16**: The system SHALL provide contextual help tooltips for all input fields.

### Maintainability

**NFR-17**: All Python code SHALL follow PEP 8 style guidelines and include docstrings.

**NFR-18**: The SageMaker model SHALL be versioned in the SageMaker Model Registry.

**NFR-19**: CloudWatch logs SHALL be retained for 30 days for debugging and audit purposes.

## Technical Constraints

**TC-1**: The focus score prediction logic MUST use AWS SageMaker with Multiple Linear Regression.

**TC-2**: The roadmap generation MUST use Amazon Bedrock (Claude 3 Sonnet or Haiku models).

**TC-3**: The system MUST be implemented using Python 3.9 or higher.

**TC-4**: All AWS resources MUST be tagged with `project: deep-work-predictor` and `hackathon: ai-for-bharat`.

**TC-5**: The solution MUST be deployable in AWS us-east-1 or ap-south-1 regions.

## Success Criteria

1. Successfully predict deep work potential with R² > 0.7 on test data
2. Generate personalized roadmaps using Bedrock with 100% success rate (including fallback)
3. Complete end-to-end prediction and roadmap generation in under 15 seconds
4. Demonstrate working system with both student and developer personas during hackathon
5. Deploy fully functional MVP on AWS infrastructure

## Out of Scope

- Mobile native applications (web-responsive only)
- Integration with third-party calendar or productivity tools
- Real-time biometric data collection (e.g., heart rate, sleep tracking devices)
- Multi-language support (English only for MVP)
- Payment or subscription features
