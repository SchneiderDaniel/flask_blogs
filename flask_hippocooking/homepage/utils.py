from datetime import datetime

def get_current_time():
    # Get the current time
    now = datetime.now()
    
    # Format the time as a string
    current_time = now.strftime("%H:%M:%S")
    
    return current_time