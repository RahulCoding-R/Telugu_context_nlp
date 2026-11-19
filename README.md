\# Telugu Context AI



A Telugu language processing application that combines transliteration, translation, tone detection, and conversational context analysis to better understand Telugu messages written in either Romanized or Telugu script.



\## Features



\- \*\*Telugu Transliteration\*\* – Converts Romanized Telugu input into Telugu script using IndicXlit.

\- \*\*Telugu to English Translation\*\* – Translates Telugu text into English using IndicTrans2.

\- \*\*Tone Detection\*\* – Detects conversational emotions and tones using a fine-tuned MuRIL model.

\- \*\*Context-Aware Tone Analysis\*\* – Uses Gemini when previous conversational context is provided, allowing tone to be interpreted in relation to the conversation.

\- \*\*Context Classification\*\* – Analyzes the relationship between the previous message and the current message using a trained context model.

\- \*\*Web Interface\*\* – Simple interface for entering messages and viewing Telugu text, English translation, detected tone, and contextual analysis.



\## System Architecture



The application uses two separate backend services.



\### Main Backend



\- Framework: FastAPI

\- Port: `8000`

\- Handles translation, tone detection, context analysis, and frontend requests.



\### Transliteration Service



\- Framework: Flask

\- Port: `5001`

\- Handles Romanized Telugu transliteration using IndicXlit.



\### Processing Pipeline



1\. User enters a message in Romanized Telugu.

2\. The transliteration service converts it into Telugu script.

3\. The Telugu text is translated into English using IndicTrans2.

4\. Tone is analyzed:

&#x20;  - MuRIL is used when no previous conversation is provided.

&#x20;  - Gemini is used when previous conversation is provided.

&#x20;  - Gemini is also used as a fallback when MuRIL returns an inconclusive result.

5\. If previous conversation is provided, the context classification model analyzes the relationship between the messages.

6\. The results are returned to the frontend.



\## Technology Stack



\- Python

\- FastAPI

\- Flask

\- PyTorch

\- Transformers

\- IndicXlit

\- IndicTrans2

\- MuRIL

\- Google Gemini API

\- HTML, CSS, JavaScript



\## Project Structure



```text

TELUGU\_CONTEXT\_AI/

│

├── backend/

│   ├── main.py

│   ├── models.py

│   ├── translation.py

│   ├── transliteration.py

│   ├── xlit\_service.py

│   └── test\_models.py

│

├── frontend/

│   └── index.html

│

├── models/

│   ├── context\_model/

│   ├── indictrans2/

│   ├── indicxlit/

│   └── multitask\_model/

│

├── requirements.txt

├── requirements-xlit.txt

├── .env.example

├── .gitignore

└── start\_app.bat

```



Model files and virtual environments are not included in this repository.



\## Environment Requirements



The project uses separate Python environments for the main backend and the transliteration service.



| Component | Requirement |

|---|---|

| Main backend | Python 3.11 |

| Transliteration service | Python 3.10 |

| Main environment | `.venv` |

| Transliteration environment | `xlit\_env` |

| Main backend port | `8000` |

| Transliteration service port | `5001` |



Both Python versions are kept separate because the transliteration dependencies and the main ML application have different dependency requirements.



\## Installation



\### 1. Clone the Repository



```bash

git clone https://github.com/RahulCoding-R/Telugu\_context\_nlp.git

cd Telugu\_context\_nlp

```



\### 2. Create the Main Python Environment



Install Python 3.11 and create the environment:



```bash

python -3.11 -m venv .venv

```



Activate it on Windows:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



If PowerShell blocks activation scripts:



```powershell

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

```



Then activate the environment again.



Install dependencies:



```bash

python -m pip install -r requirements.txt

```



\### 3. Create the Transliteration Environment



Install Python 3.10 separately.



Create the environment:



```bash

python -3.10 -m venv xlit\_env

```



Install transliteration dependencies:



```bash

.\\xlit\_env\\Scripts\\python.exe -m pip install -r requirements-xlit.txt

```



\### 4. Configure the Gemini API



Create a `.env` file in the project root.



```env

GEMINI\_API\_KEY=your\_gemini\_api\_key

```



Obtain your API key through Google AI Studio.



Never commit your actual `.env` file or API key.



\### 5. Configure Model Files



Pretrained and fine-tuned model assets are not included in this repository.



Place the required model files in the corresponding directories under `models/`:



\- `models/multitask\_model/` – Fine-tuned MuRIL tone detection model

\- `models/context\_model/` – Context classification model

\- `models/indictrans2/` – Translation model assets

\- `models/indicxlit/` – Transliteration model assets, if required by the local configuration



Ensure that the model paths in the backend configuration match the locations of the downloaded model files.



\## Running the Application



The application requires both backend services to be running.



\### Terminal 1 – Transliteration Service



From the project root:



```powershell

.\\xlit\_env\\Scripts\\python.exe .\\backend\\xlit\_service.py

```



The service runs at:



```text

http://127.0.0.1:5001

```



\### Terminal 2 – Main Backend



Activate the main environment:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Start FastAPI:



```bash

python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

```



The web application is available at:



```text

http://127.0.0.1:8000

```



Both services must remain running while using the application.



Alternatively, `start\_app.bat` can be used if configured for the local environment.



\## API



\### Endpoint



`POST /api/process`



\### Request



```json

{

&#x20; "text": "ela unnavu",

&#x20; "previous\_message": ""

}

```



\### Parameters



| Parameter | Type | Description |

|---|---|---|

| `text` | String | Current message in Romanized Telugu |

| `previous\_message` | String | Optional previous conversation in Telugu |



\### Response



```json

{

&#x20; "input": "ela unnavu",

&#x20; "telugu": "ఎలా ఉన్నావు",

&#x20; "english": "How are you?",

&#x20; "tone": "happy",

&#x20; "tone\_confidence": 0.94,

&#x20; "tone\_source": "MuRIL",

&#x20; "context\_analysis": null

}

```



The response values above are illustrative.



\## Tone Detection Logic



\### Without Previous Conversation



MuRIL predicts the tone of the current Telugu message.



If the model produces an inconclusive prediction, Gemini is used as a fallback.



\### With Previous Conversation



Gemini analyzes the previous conversation and the current message together to determine the current message's tone.



This allows the interpretation of conversational messages that may depend on context, such as short replies, ambiguous expressions, or responses whose emotional meaning changes depending on the previous message.



\## Notes



\- The Gemini API is required for context-based tone detection and fallback analysis.

\- Model assets must be available locally before the application can run successfully.

\- The transliteration service and main backend run independently.

\- The application is currently configured for local execution on Windows.

\- API usage and availability are subject to the provider's limits and policies.



\## Disclaimer



Tone and context predictions are machine-generated interpretations of language. They may not accurately represent the speaker's intended emotion or meaning, especially in informal conversations, sarcasm, slang, or ambiguous messages.



