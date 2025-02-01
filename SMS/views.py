# from twilio.rest import Client
# from dotenv import load_dotenv
# import os
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.shortcuts import render, redirect
#
# load_dotenv()
#
# # twilio secrets
# sid = os.getenv("account_sid")
# token = os.getenv("auth_token")
# service_sid = os.getenv("service_sid")
#
# client = Client(sid, token)
#
#
# def send_verification_code(phone_number):
#     verification = client.verify.v2.services(service_sid).verifications.create(
#         to="+8201056029289",
#         channel="sms"
#     )
#     return verification.status
#
#
#
# def check_verification_code(phone_number, code):
#     verification_check = client.verify.v2.services(service_sid).verification_checks.create(
#         to=phone_number,
#         code=code
#     )
#     return verification_check.status  # "approved" if the code is correct
#
#
# def verify_phone(request):
#     if request.method == "POST":
#         phone_number = request.session.get("phone_number")
#         user_data = request.session.get("user_info")
#         code = request.POST.get("code")
#
#         if not phone_number or not user_data:
#             messages.error(request, "Session expired! Please try again 🙌")
#             return redirect("register")
#
#         # save user if the code is correct
#         if check_verification_code(phone_number, code) == "approved":
#             user = User(**user_data)
#             user.save()
#
#             # erase users' details
#             del request.session["phone_number"]
#             del request.session["user_info"]
#             return redirect("login")
#         else:
#             messages.error(request, "Invalid code. Please try again.")
#
#     return render(request, "users/verification.html")
#
#
