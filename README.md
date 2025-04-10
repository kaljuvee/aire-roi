# AIRE ROI Bot

AI-powered chatbot for calculating and analyzing ROI for AI and robotics investments.

## Features

- Calculate ROI metrics (NPV, IRR, Payback Period)
- Analyze economic effects of AI/robotics investments
- Provide examples and guidance
- Explain financial concepts in simple terms
- Support for Estonian language

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Mistral API key:
   ```
   MISTRAL_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run Home.py
   ```
2. Open your browser and navigate to the provided URL
3. Start chatting with the bot about your AI/robotics investment

## Project Structure

- `Home.py`: Main Streamlit interface
- `agent/`: Contains the LangGraph agent implementation
  - `agent.py`: Agent configuration and setup
  - `tools.py`: Custom tools for ROI calculations and web search

## License

MIT License