import sys
import logging

# Activate the virtual environment (if you are using one)
# activate_this = '/path/to/your/virtualenv/bin/activate_this.py'
# with open(activate_this) as file_:
# exec(file_.read(), dict(__file__=activate_this))

# Adjust the path to your application
sys.path.insert(0, '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship')


# sys.path.insert(0, '/var/www/fellowship/fellowship/BartiFellowship/BartiFellowship')


from app import app as application
# Import your Flask app instance

# Configure logging if needed
# For example, you can set up a log file:
# logging.basicConfig(filename='/path/to/your/log/file.log', level=logging.INFO)

# Optionally, configure additional settings here if needed

if __name__ == "__main__":
    application.run()
