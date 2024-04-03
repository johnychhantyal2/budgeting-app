# My FastAPI Project

This is a simple guide on how to set up and run a FastAPI project using Python virtualenv.

## Prerequisites

- Python 3.x installed on your machine
- pip package manager

## Setup

1. Clone the project repository:

   ```bash
   git clone https://github.com/johnychhantyal2/budgeting-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd budgeting-app
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - For Windows:

     ```bash
     venv\Scripts\activate
     ```

   - For macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

1. Start the FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

2. Open your web browser and navigate to `http://localhost:8000` to access the API.

## Additional Notes

- To deactivate the virtual environment, simply run:

  ```bash
  deactivate
  ```

- Refer to the FastAPI documentation for more information on building your API: [FastAPI Documentation](https://fastapi.tiangolo.com/)
