README for Multi-Language Image Analysis Flask App

🌐 Overview

Technical Explanation

This Flask application integrates with OpenAI's GPT-4 Vision model to analyze images and provide insights based on user queries. It supports multiple languages (English and French) for input and responses.
The app uses environment variables to securely manage sensitive data like the OpenAI API key. Key features include image resizing, base64 encoding for image transmission, and dynamic content rendering based on language selection. The app is container-ready with Docker configurations.

Non-Technical Explanation

Our app is like a smart assistant that understands images and answers your questions about them in English or French. 🤖🎨

You can upload an image, ask a question, and it will give you a detailed response. It's easy to use and is designed with privacy and efficiency in mind. 🌍🔒

🚀 Getting Started

Prerequisites

    Python 3.6 or later
    Flask
    PIL (Python Imaging Library)
    requests library
    dotenv for managing environment variables

Installation

Clone the repository:

    git clone [REPO_URL]

Navigate to the app's directory:

    cd path/to/app

Install dependencies:

    pip install -r requirements.txt

Set up your .env file with your OpenAI API key:

makefile

    OPENAI_API_KEY=your_api_key_here

Running the App

Run the Flask app:

    python multi-lang-app.py

Access the app in a web browser at http://localhost:5000.

🖼️ Using the App

Choose your language (English or French).
Upload an image and ask a question related to it.
Get an insightful response based on advanced AI analysis. 🧠💡

🔧 Docker Support

Build the Docker image:

    docker build -t multi-lang-app .

Run the Docker container:

    docker run -p 5000:5000 multi-lang-app

