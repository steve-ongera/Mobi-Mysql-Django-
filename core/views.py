from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Account, Transaction
from django.contrib import messages
from decimal import Decimal  # Import Decimal for type conversion
from django.contrib import messages
from .forms import CustomRegistrationForm
from django.contrib.auth import login, authenticate ,logout



@login_required
def dashboard(request):
    # Get the logged-in user
    user = request.user

    # Retrieve the account associated with the logged-in user
    account = Account.objects.get(user=user)

    # Get transactions related to the user (as sender or receiver)
    transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)
    transactions = transactions.order_by('-timestamp')  # Sort by timestamp (most recent first)

    recent_transactions = transactions[:2]  # Get the 2 most recent transactions

    context = {
        'account': account,
        'recent_transactions': recent_transactions,
        'transactions': transactions,
    }

    return render(request, 'dashboard.html', context)

@login_required
def deposit(request):
    if request.method == 'POST':
        try:
            # Get the amount from the POST request and ensure it is a valid Decimal
            amount = Decimal(request.POST['amount'])
            
            # Validate that the amount is positive
            if amount <= 0:
                messages.error(request, 'Amount must be greater than 0.')
                return redirect('deposit')
            
            # Get the account of the logged-in user
            account = Account.objects.get(user=request.user)
            
            # Add the amount to the user's account balance
            account.balance += amount
            account.save()

            # Record the deposit transaction (no receiver for deposit)
            transaction = Transaction(
                sender=request.user,  # The user performing the deposit
                receiver=None,         # No receiver for deposit
                amount=amount
            )
            transaction.save()  # Save the transaction record

            # Success message after depositing
            messages.success(request, f'Deposit of Ksh {amount} successful!')
            return redirect('dashboard')

        except KeyError:
            messages.error(request, 'Invalid request data. Please ensure the amount is provided.')
        except Account.DoesNotExist:
            messages.error(request, 'Account not found.')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'deposit.html')

@login_required
def withdraw(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST['amount'])  # Convert amount to Decimal
            if amount <= 0:
                messages.error(request, 'Amount must be greater than 0.')
                return redirect('dashboard')

            account = Account.objects.get(user=request.user)

            if account.balance < amount:
                messages.error(request, 'Insufficient balance.')
                return redirect('dashboard')

            # Subtract the amount from the account balance
            account.balance -= amount
            account.save()

            # Record the withdrawal as a transaction
            transaction = Transaction(
                sender=request.user,  # User is both sender and the account holder
                receiver=None,        # For withdrawal, there is no recipient
                amount=amount
            )
            transaction.save()

            messages.success(request, f'You have successfully withdrawn Ksh {amount}!')
            return redirect('dashboard')

        except Account.DoesNotExist:
            messages.error(request, 'Account not found.')
        except KeyError:
            messages.error(request, 'Invalid request data.')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
    
    return render(request, 'withdraw.html')

@login_required
def send_money(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST['amount'])  # Convert amount to Decimal
            recipient_username = request.POST['recipient']
            
            # Validate input
            if amount <= 0:
                messages.error(request, 'Amount must be greater than 0.')
                return redirect('send_money')

            # Get sender's account
            sender_account = Account.objects.get(user=request.user)
            
            if sender_account.balance < amount:
                messages.error(request, 'Insufficient balance.')
                return redirect('send_money')

            # Get recipient's account
            recipient_account = Account.objects.get(user__username=recipient_username)

            # Perform the transaction
            sender_account.balance -= amount  # Subtract from sender's account
            recipient_account.balance += amount  # Add to recipient's account
            sender_account.save()
            recipient_account.save()

            # Record the transaction
            transaction = Transaction(
                sender=request.user,
                receiver=recipient_account.user,
                amount=amount
            )
            transaction.save()

            messages.success(request, f'Successfully sent Ksh {amount} to {recipient_username}!')
            return redirect('dashboard')

        except Account.DoesNotExist:
            messages.error(request, 'Recipient account not found.')
        except KeyError:
            messages.error(request, 'Invalid request data.')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
    
    return render(request, 'send_money.html')




def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set hashed password
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('dashboard')  # Redirect to the dashboard or home page
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'auth/login.html')



def custom_logout(request):
    # Log the user out
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')  # Redirect to login page or any other page


@login_required
def account_details(request):
    """View to display user details."""
    user = request.user
    context = {
        'user': user,  # Pass the user object to the template
    }
    return render(request, 'account.html', context)
