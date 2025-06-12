# import jwt
# import requests
# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from django.contrib.auth.models import User

# # Define a secret key for decoding JWT tokens
# SECRET_KEY = "skillup-online"

# # Define a custom authentication class
# class CustomAuthentication(BaseAuthentication):

#     # Define an authenticate method
#     def authenticate(self, request):

#         # Get the JWT token from the request header
#         token = request.META.get("HTTP_AUTHORIZATION")

#         # Decode the token using the secret key
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed("Invalid token")

#         # Get the Nm id and college id from the payload
#         email = payload.get("email")
#         id = payload.get("id")

#         # If either are not passed, raise an exception
#         if not email or not id:
#             raise AuthenticationFailed("Missing Nm id or college id")

#         # Check if the user exists in the database by querying with the Nm id
#         user = User.objects.filter(email=email).first()

#         # If not, create a new user with the input data
#         # if not user:
#         #     email = request.data.get("email")
#         #     first_name = request.data.get("first_name")
#         #     last_name = request.data.get("last_name")
#         #     user = User.objects.create(nm_id=nm_id, email=email, first_name=first_name, last_name=last_name)

#         # Use the requests module to make a POST request to the api with the user's Nm id and course id as parameters
#         response = requests.post(f"http://127.0.0.1:8000/ibm3/user/", data={"email": "rajkumarwgl55@gmail.com", "id": })

#         # Return the user and token as a tuple
#         return (user, token)