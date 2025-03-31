# JOSEF_MUSCAT_DGD_6.2A_DE

Clone the Directory:
git clone https://github.com/Verdarin/JOSEF_MUSCAT_DGD_6.2A_DE
 
Open Project ROOT Repository Directory on VSCode

Terminal -> New Terminal

if needed delete the existing environment and

Create new Virtual Environment:
    python -m venv env

Activate Virtual Environment:
    Windows: env\Scripts\activate
    MacOS: source env/bin/activate

Install Required Deprendencies:
    pip install -r requirements.txt

If you are running the server locally add MONGODB_URI to your environement variables with your MONGODB Connection String

Start the Server: uvicorn project.main:app --reload (if running locally)

TEST_INJECTIONS_DATA has .mp3, sprite pngs and json data to feed into postman for testing.