import sys
from .helpers import log

# Step 3: Check the 8 cases (Add, Modify, Delete)
def checkAction(src_url, loc_eq_dst, location, action, logging_file_path):
    action = action.lower()
    
    if location:
        if action == 'add':
            if loc_eq_dst == False:
                if (location != src_url):
                    # Case 2. Add & Destination!=Location & Location!=SourceURL --> Did you mean MODIFY ?
                    log(f"{src_url} is redirected to {location}", logging_file_path)
                    action = 'modify'
                    log(f"ADD action changed to: {action.upper()}", logging_file_path)
            else:
                # Case 1. Add & Destination==Location --> No need to ADD
                action = False
                log("No need to ADD. Already Redirected to Destination.", logging_file_path)
        elif action == 'modify':
            if loc_eq_dst == False:
                if (location == src_url):
                    # Case 5. Modify & Destination!=Location & Location==SourceURL --> Did you mean ADD ?
                    log(f"{src_url} is redirected to {location}", logging_file_path)
                    action = 'add'
                    log(f"MODIFY action changed to: {action.upper()}", logging_file_path)
            else:
                # Case 4. Modify & Destination==Location --> No need to MODIFY
                action = False
                log("No need to MODIFY. Already Redirected to Destination.", logging_file_path)
        else:
            if loc_eq_dst == False:
                # Case 7. Delete & Destination!=Location --> No need to DELETE
                action = False
                log("No need to DELETE. Redirection to the Destination does not exist.", logging_file_path)
        # Case 3(add), Case 6(modify), Case 8(delete) --> Proceed with inital action    

        if action == False:
            log("This Action is not appropriate in current Redirection situation", logging_file_path)
        
        return action 
    
    else: # Case 9: 404 Error (location == None)
        return action