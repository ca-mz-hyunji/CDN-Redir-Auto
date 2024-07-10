# Coding Step-by-Step for Developers
## Non-csv file method (for single redirection)
### Phase 1 - Before Updating Config File
1. Get inputs from User
2. Send Curl (check Destination & make a log if there wasn't)
3. Check the 8 cases (Add, Modify, Delete)
    1. Add & Destination==Location
        * No need to ADD
    2. Add & Destination!=Location & Location!=SourceURL
        * Need to check action again -> Did you mean MODIFY ?
    3. Add & Desitnation!=Location & Location==SourceURL
        * Good to ADD
    4. Modify & Destination==Location
        * No need to MODIFY
    5. Modify & Destination!=Location & Location==SourceURL
        * Need to check action again -> Did you mean ADD ?
    6. Modify & Destination!=Location & Location!=SourceURL
        * Good to MODIFY
    7. Delete & Destination!=Location
        * Mo need to DELETE
    8. Delete & Destination==Location
        * Good to DELETE
4. Grep Command --> Find Log Files (sort into shortest first)
5. Open the (shortest) log file (don't use /origin.log) and find Virtual Hostname for Path_from
6. Find BaseHost for the Virtual Hostname (from /usr/local/m2/setting.json)
7. Open the JSON config file (located at BaseHost) and search for redirection rule (using Path_from)
    1. Modify & redirection rule exists
        * Good to MODIFY 
    2. Modify & redirection rule does NOT exist
        * Go back to Step 5 (try next log file)
    3. Delete & redirection rule exists
        * Good to DELETE
    4. Delete & redirection rule does NOT exist
        * Go back to Step 5 (try next log file)
    5. Add & redirection rule does NOT exist
        * Good to ADD

### Phase 2 - Updating Config File & Deploy
8. (*) Show redirection rule (pattern) to Add/Modify/Delete & Check user confirmation for updating the config file
9. (*) Copy a backup file in a subdirectory
10. (*) Update the Config File with redirection rule
11. (*) Deploy
12. (*) Test the redirection change by using Curl (every 2 minutes, 5 times max)
    * If Location==Path_from
        1. Show Curl output for user to see
        2. Exit code
    * If timeout, Ask user one of 3 choices:
        1. Roll-back (using backup file) and Exit code (let user manually do the redirection) 
        2. Wait another 10 minutes
        3. Exit code without roll-back 


## csv file method (for multiple redirections)
