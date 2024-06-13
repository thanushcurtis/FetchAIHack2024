import os

if __name__ == "__main__":
    os.system("gunicorn -w 4 -b 0.0.0.0:8080 -t 300 project.wsgi:application")