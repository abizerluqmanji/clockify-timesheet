# Clockify Time Entries

Steps to use the script:
1. Install the required python packages in a venv using `pip install -r requirements.txt`
2. Obtain a Clockify API key from your Clockify account and save it in an environment variable named `CLOCKIFY_API_KEY`.
3. Update the `PROJECT_ID` variables in the script with one for your project.
4. Run the script using `python time_entry.py`.

Sample usage:
```sh
python time_entry.py --commit
```