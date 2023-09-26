from decouple import config

with open("/Users/jober/PythonProjects/django-server-playground/.env", "r") as f:
    print("Contents of .env:")
    print(f.read())

FACEBOOK_APP_ID = config("FACEBOOK_APP_ID", default="NOT FOUND")
print("\nValue of FACEBOOK_APP_ID:", FACEBOOK_APP_ID)
