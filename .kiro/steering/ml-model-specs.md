---
inclusion: fileMatch
fileMatchPattern: "**/model/**,**/notebooks/**,**/*model*.py"
---

# ML Model Specifications

## Model Type
Multiple Linear Regression for interpretability and fast inference

## Input Features
Consider these feature categories:
- **Temporal**: Time of day, day of week, season
- **Environmental**: Noise level, lighting, workspace type
- **Behavioral**: Sleep hours, exercise, caffeine intake, previous deep work sessions
- **Cognitive**: Task complexity, context switches, meeting load
- **Physiological**: Self-reported energy level, stress score

## Target Variable
Deep Work Potential Score (0-100 scale)
- 0-30: Low potential (high distraction risk)
- 31-70: Moderate potential (requires optimization)
- 71-100: High potential (optimal conditions)

## Model Training
- **Algorithm**: sklearn.linear_model.LinearRegression or SageMaker Linear Learner
- **Train/Test Split**: 80/20 with stratification
- **Validation**: 5-fold cross-validation
- **Metrics**: R², RMSE, MAE

## Feature Engineering
- Normalize continuous features (StandardScaler)
- One-hot encode categorical variables
- Create interaction terms for key feature pairs
- Handle missing values with median imputation

## SageMaker Configuration
```python
estimator = LinearLearner(
    role=sagemaker_role,
    instance_count=1,
    instance_type='ml.m5.xlarge',
    predictor_type='regressor',
    normalize_data=True
)
```

## Model Evaluation Criteria
- R² > 0.7 for production deployment
- RMSE < 15 points on test set
- No significant bias across user demographics
- Inference latency < 100ms
