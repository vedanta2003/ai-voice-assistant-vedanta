# AI Voice Assistant API

This repository hosts a FastAPI-based AI Voice Assistant capable of processing voice and text inputs to detect intents, interact with OpenAI for advanced natural language understanding, and log interactions in MongoDB.

![Docker](https://img.shields.io/badge/Docker-✔️-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-✔️-green) ![MongoDB](https://img.shields.io/badge/MongoDB-✔️-green)

## 🚀 Features
- 🗣 **Voice & Text Input:** Convert speech to text using Google Speech Recognition or process direct text inputs.
- 📚 **Intent Recognition:** Use simple keyword matching or leverage OpenAI's GPT-3.5 for sophisticated intent detection.
- 📈 **Interaction Logging:** Save and retrieve interactions with timestamps in MongoDB.
- 📘 **FastAPI Documentation:** Auto-generated API docs available at `/docs`.

## 📂 Project Structure
```
├── Dockerfile
├── app.py
├── .env
├── requirements.txt
└── README.md
```

## 🛠️ Installation & Running the Project

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant
```

### 2. Set Up Environment Variables
Create a `.env` file with the following:
```
MONGO_CONNECTION_STRING=mongodb://your-mongodb-uri
OPENAI_API_KEY=your-openai-api-key
```

### 3. Build and Run with Docker
```sh
docker build -t ai-voice-assistant .
docker run -d -p 8000:8000 --env-file .env ai-voice-assistant
```

Or pull directly from Docker Hub:
```sh
docker pull yadavvedanta19/ai-voice-assistant2
docker run -d -p 8000:8000 --env-file .env yadavvedanta19/ai-voice-assistant2
```

### 4. Access the API
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view and interact with the API.

## 🛡️ API Endpoints
- `GET /` — Welcome message.
- `GET /health` — API health check.
- `POST /recognize-intent` — Recognize intent from text input.
- `POST /voice-input` — Recognize intent from voice input.
- `GET /interactions` — Fetch logged interactions.

Example request to recognize intent:
```sh
curl -X POST http://localhost:8000/recognize-intent \
-H "Content-Type: application/json" \
-d '{"text": "What’s the weather like today?"}'
```

## 🏁 Deployment
Deploy to a cloud provider (AWS, GCP, Azure) with Docker or Kubernetes. Let me know if you’d like help setting that up! 🚀

---

### 🧑‍💻 Author
**Vedanta Yadav**

Happy coding! 💡 Let me know if you want to add more sections or refine anything! 🚀

