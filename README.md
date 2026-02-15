# Deep-Work-Predictor
Track: AI for Learning & Developer Productivity

Built for: AI for Bharat Hackathon 2026

📖 Overview
The Deep-Work Potential Predictor is an AI-powered productivity ecosystem designed to help students and developers master their focus. By predicting your Focus Score (0-100) using biometric and environmental data, the app intelligently schedules your hardest tasks (like debugging or math) during your peak cognitive windows.

Key Features
Predictive Scheduling: Uses Multiple Linear Regression to calculate your "Flow State" probability.

AI Roadmap Generator: Converts long-term goals (e.g., Andrew Ng’s ML course) into manageable daily "bits."

Smart To-Do List: Automatically prioritizes tasks based on your predicted focus score.

Focus Guard: Integrated app-blocking logic to minimize distractions during high-focus periods.

🛠 Tech Stack
This project is built following the AWS Well-Architected Framework:

Generative AI: Amazon Bedrock (Claude 3.5 Sonnet) for Roadmap Synthesis.

Machine Learning: Amazon SageMaker for Focus Score regression modeling.

Compute: AWS Lambda (Serverless Backend).

Database: Amazon DynamoDB for persistent storage of user vitals.

Dev Tools: Amazon Q & Kiro AI IDE (Mandatory Spec-Driven Development).

📐 Spec-Driven Development
To ensure architectural integrity, this project strictly followed the Kiro workflow:

requirements.md: Functional specs defined using EARS notation.

design.md: Technical blueprint and system data flow.

.kiro/: Mandatory compliance directory tracking the development lifecycle.

🚀 Getting Started
Clone the repo:

Bash
git clone https://github.com/IshaanMogs/Deep-Work-Potential-Predictor.git
Review the Specs: Check requirements.md and design.md to understand the system logic.

Authors
Ishaan Kumar - Lead Developer & Architect
