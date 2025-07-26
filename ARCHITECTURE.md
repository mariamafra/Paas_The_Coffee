# Chiller - Smart Recipe Suggester Architecture

## 1. High-Level System Design

The Chiller application is designed as a web-based interface built with Streamlit, which orchestrates calls to the Google Gemini API. The flow involves a user uploading an image, the application processing it with Gemini to identify ingredients, and then generating recipe suggestions based on those ingredients, all displayed back to the user.

Here's a high-level component diagram:

![alt text](<Untitled diagram _ Mermaid Chart-2025-07-25-233652.png>)
## 2. Component Breakdown and Responsibilities

### 2.1. Streamlit Application (`src/app.py`)

This is the core of the Chiller system, acting as both the **UI Layer** and the **Orchestration / Executor Layer**.

*   **User Interface (UI) Management:**
    *   Handles image uploads from the user.
    *   Displays the uploaded image.
    *   Presents identified ingredients to the user.
    *   Renders the generated recipe suggestions.
    *   Manages basic user interaction elements (buttons, text areas).

*   **Planner & Executor:**
    *   The Streamlit app acts as a **simple Planner** by defining the sequence of AI interactions: First, ingredient identification; then, recipe generation. It crafts the specific prompts for each stage based on the user's input and previous AI responses.
    *   It acts as the **Executor** by initiating the API calls to the Google Gemini API and processing their responses. It translates user actions into AI model requests and model responses back into user-friendly output.

*   **Memory Structure (Ephemeral/Stateless per Request):**
    *   The application's memory is largely ephemeral within a single user request.
    *   The `uploaded_file` (PIL Image object) is held in memory temporarily.
    *   The `identification_response.text` (raw identified ingredients) and `ingredients_list` (parsed list) serve as a temporary "scratchpad memory" that is used to formulate the subsequent recipe generation prompt.
    *   There is **no persistent session memory** or user profile storage across different user interactions or browser sessions. Each interaction is treated as a new, independent request.

### 2.2. Google Gemini API

This serves as the primary **Tool Integration** for the AI capabilities of Chiller.

*   **Model Used:** `gemini-1.5-flash`
    *   **Vision Capability:** Utilized for identifying ingredients from the uploaded images. This is where the model's multimodal understanding comes into play.
    *   **Text Generation Capability:** Employed to generate creative recipe suggestions and detailed instructions based on the list of identified ingredients.

*   **Role in the System:** The Gemini API acts as a powerful external "brain" that provides the core intelligence for image analysis and creative text generation. The Streamlit app simply queries this brain and displays its insights.

### 2.3. Tool Integrations

*   **Google Gemini API:** (Already detailed above) This is the sole external AI model integration.
*   **PIL (Pillow):** Used for opening and processing the uploaded image files (`PIL.Image.open`).
*   **`os` module:** Used for accessing environment variables (specifically `GEMINI_API_KEY`).
*   **`python-dotenv`:** (Local development only) Used for loading environment variables from a `.env` file, facilitating secure API key management during development.

## 3. Logging and Observability

The current implementation provides basic logging and observability mechanisms suitable for a hackathon project:

*   **Streamlit UI Messages:**
    *   `st.info()`: Provides informative messages to the user (e.g., "Analyzing your image...", "Generating recipe suggestions...").
    *   `st.success()`: Indicates successful operations (e.g., "Identified Ingredients: ...").
    *   `st.warning()`: Alerts the user to non-critical issues (e.g., "Could not identify significant ingredients...").
    *   `st.error()`: Displays critical error messages to the user (e.g., API key issues, processing failures).

*   **Standard Output/Error:**
    *   Errors caught within `try-except` blocks are printed to the Streamlit console/terminal where the application is running, providing internal debugging information.
    *   The `print()` statements outside the Streamlit app (e.g., in the Colab notebook setup) provide setup and Ngrok tunnel information.

For a production-grade application, this would be expanded to include:
*   Structured logging to a file or a centralized logging service.
*   Performance monitoring of API calls and Streamlit render times.
*   Error tracking and alerting.
*   Potentially, usage analytics.