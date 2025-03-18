# JOSEF_MUSCAT_DGD_6.2A_DE
 
Open Project ROOT Repository Directory on VSCode

Terminal -> New Terminal

Activate Virtual Environment:
    Windows: env\Scripts\activate
    MacOS source env/bin/activate

Install Required Deprendencies:
    pip install -r requirements.txt


Go to project/database.py and change the client connection string to your Mongo Atlas Cluster connection String.

Start the Server:
    uvicorn project.main:app --reload

TEST_INJECTIONS_DATA has a .mp3, and a .png sprite to use when posting with POSTMAN