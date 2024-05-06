# library/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import csv
from .forms import AddBookForm, AddUser
from .models import Book, User

def login(request):
    if request.method == 'POST':
        form = AddUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Hardcoded sample data for user authentication
            sample_users = {
                'admin': {'username': 'admin', 'password': 'admin123', 'user_type': 'admin'},
                'regular': {'username': 'user', 'password': 'user123', 'user_type': 'regular'}
            }
            if username in sample_users and sample_users[username]['password'] == password:
                user_data = sample_users[username]
                request.session['user'] = {
                    'username': user_data['username'],
                    'user_type': user_data['user_type']
                }
                return redirect('home')
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=400)
    else:
        form = AddUser()
    return render(request, 'login.html', {'form': form})

def home(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')

    books = []
    if user['user_type'] == 'admin':
        with open('data/adminUser.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                books.append(row['Book Name'])
    else:
        with open('data/regularUser.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                books.append(row['Book Name'])

    return JsonResponse({'books': books})

def add_book(request):
    user = request.session.get('user')
    if not user or user['user_type'] != 'admin':
        return JsonResponse({'message': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            book_name = form.cleaned_data['name']
            author = form.cleaned_data['author']
            publication_year = form.cleaned_data['publication_year']
            # Validating parameters
            if not all([isinstance(val, str) for val in [book_name, author]]):
                return JsonResponse({'message': 'Book name and author should be strings'}, status=400)
            if not isinstance(publication_year, int):
                return JsonResponse({'message': 'Publication year should be a number'}, status=400)
            # Adding the book to the appropriate CSV file
            with open('regularUser.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([book_name, author, publication_year])
            # Fetch the updated list of books from the CSV file
            updated_books = []
            with open('regularUser.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    updated_books.append(row)
            # Pass the updated books list to the template rendering the home page
            return render(request, 'home.html', {'books': updated_books})
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    form = AddBookForm()
    return render(request, 'add_book.html', {'form': form})
def delete_book(request):
    user = request.session.get('user')
    if not user or user['user_type'] != 'admin':
        return JsonResponse({'message': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        if not book_name:
            return JsonResponse({'message': 'Book name is required'}, status=400)

        # Deleting the book from the regularUser.csv file
        with open('regularUser.csv', 'r') as file:
            lines = file.readlines()

        with open('regularUser.csv', 'w') as file:
            writer = csv.writer(file)
            for line in lines:
                if line.strip('\n') != book_name:
                    writer.writerow([line.strip('\n')])

        return redirect('home')

    return JsonResponse({'message': 'Method not allowed'}, status=405)
