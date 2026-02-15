---
inclusion: always
---

# Deep-Work Potential Predictor - Project Overview

## Project Context
AI for Bharat Hackathon submission - A system that predicts deep work potential using machine learning and generates personalized productivity roadmaps.

## Core Technologies
- **AWS SageMaker**: Multiple Linear Regression model training and deployment
- **AWS Bedrock**: AI-powered roadmap generation based on predictions
- **Python**: Primary development language

## Architecture Components
1. **Data Pipeline**: Collect and preprocess user productivity metrics
2. **ML Model**: Multiple Linear Regression on SageMaker for deep-work potential scoring
3. **Prediction Service**: Real-time inference endpoint
4. **Roadmap Generator**: Bedrock integration for personalized recommendations

## Key Objectives
- Predict user's deep work potential based on behavioral and environmental factors
- Generate actionable, personalized productivity roadmaps
- Deploy scalable ML infrastructure on AWS
- Deliver hackathon-ready MVP

## Project Structure
- `/data`: Training datasets and preprocessing scripts
- `/model`: SageMaker training scripts and model artifacts
- `/api`: Prediction service and Bedrock integration
- `/notebooks`: Exploratory analysis and model development
- `/infrastructure`: AWS resource configurations (CloudFormation/Terraform)
