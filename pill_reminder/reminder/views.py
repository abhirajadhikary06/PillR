from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import preprocess_image, extract_text_from_image, clean_text, refine_text_with_gemini
from .task import process_prescription
from django.shortcuts import render, redirect
from pill_reminder.settings import supabase, account
from appwrite.exception import AppwriteException

def appwrite_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            # Check if the user has an active session
            from pill_reminder.settings import account
            session = account.get_session(session_id='current')
            return view_func(request, *args, **kwargs)
        except AppwriteException:
            # Redirect to login if no active session exists
            return redirect('login')
    return wrapper

@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')

        try:
            # Create a new user in Appwrite
            response = account.create(email=email, password=password, name=name)
            return JsonResponse({"message": "User registered successfully.", "user_id": response['$id']})
        except AppwriteException as e:
            return JsonResponse({"error": str(e.message)}, status=400)

    return render(request, 'register.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Log in the user and create a session
            response = account.create_email_session(email=email, password=password)
            return JsonResponse({"message": "Login successful.", "session_id": response['$id']})
        except AppwriteException as e:
            return JsonResponse({"error": str(e.message)}, status=400)

    return render(request, 'login.html')


@appwrite_login_required
def logout(request):
    try:
        # Delete the current session
        account.delete_session(session_id='current')
        return JsonResponse({"message": "Logged out successfully."})
    except AppwriteException as e:
        return JsonResponse({"error": str(e.message)}, status=400)
    
@appwrite_login_required
@csrf_exempt
def set_reminder(request):
    if request.method == 'POST' and request.FILES.get('prescription'):
        try:
            # Get the logged-in user's ID
            user = account.get()
            user_id = user['$id']

            # Save the uploaded file temporarily
            uploaded_file = request.FILES['prescription']
            image_path = f"/tmp/{uploaded_file.name}"
            with open(image_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Process the prescription asynchronously
            process_prescription.delay(image_path, user_id)

            return JsonResponse({"message": "Prescription uploaded successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return render(request, 'set_reminder.html')

@appwrite_login_required
def dashboard(request):
    try:
        # Check if the user is logged in
        session = account.get_session(session_id='current')
        user = account.get()
        user_id = user['$id']

        # Fetch prescriptions for the logged-in user
        response = supabase.table('prescriptions').select('*').eq('user_id', user_id).execute()
        prescriptions = response.data

        return render(request, 'dashboard.html', {'user': user, 'prescriptions': prescriptions})
    except AppwriteException:
        return redirect('login')
    
def share_prescription(request, prescription_id):
    try:
        # Fetch the prescription by ID
        response = supabase.table('prescriptions').select('*').eq('id', prescription_id).execute()
        prescription = response.data[0]

        # Generate a shareable link (you can use a service like ngrok or host the app publicly)
        share_link = f"http://yourdomain.com/view-prescription/{prescription_id}/"

        return render(request, 'share_prescription.html', {'share_link': share_link})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def view_prescription(request, prescription_id):
    try:
        # Fetch the prescription by ID
        response = supabase.table('prescriptions').select('*').eq('id', prescription_id).execute()
        prescription = response.data[0]

        return render(request, 'view_prescription.html', {'prescription': prescription})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)