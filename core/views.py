from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from decimal import Decimal  # Import Decimal for type conversion
from django.contrib import messages
from .forms import *
from django.contrib.auth import login, authenticate ,logout
from django.db.models import Count


@login_required
def dashboard(request):
    # Get the logged-in user
    user = request.user

    # Retrieve the account associated with the logged-in user
    account = Account.objects.get(user=user)

    # Retrieve the Fuliza instance associated with the account
    fuliza = Fuliza.objects.get(account=account)

    # Get transactions related to the user (as sender or receiver)
    transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)
    transactions = transactions.order_by('-timestamp')  # Sort by timestamp (most recent first)

    recent_transactions = transactions[:2]  # Get the 2 most recent transactions

    # Calculate available Fuliza
    available_fuliza = fuliza.limit - fuliza.used

    context = {
        'account': account,
        'fuliza': fuliza,
        'available_fuliza': available_fuliza,
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
            messages.success(request, f"Welcome back, {user.username}!")
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

@login_required
def transact(request):
    user = request.user
    
    # Get the most frequent receiver of transactions by the logged-in user
    frequent_contact = (
        Transaction.objects.filter(sender=user, receiver__isnull=False)
        .values('receiver__first_name', 'receiver__last_name')
        .annotate(count=Count('receiver'))
        .order_by('-count')
        .first()
    )

    context = {
        'frequent_contact': frequent_contact,
    }
    return render(request, 'transact.html', context)


@login_required
def search(request):
    return render(request, 'search.html')


@login_required
def deposit_funds(request):
    user = request.user
    
    try:
        # Fetch the MShwari account for the current user
        mshwari_account = MShwari.objects.get(account__user=user)
    except MShwari.DoesNotExist:
        # If the user does not have an MShwari account, show an error message
        messages.error(request, "You do not have a MShwari account.")
        return redirect('create_mshwari_account')  # Redirect to a page to create an MShwari account

    if request.method == "POST":
        # Get the deposit amount from the form
        try:
            amount = float(request.POST.get('amount', 0))  # Get as float
            amount = Decimal(amount)  # Convert to Decimal
        except ValueError:
            amount = Decimal(0)  # Handle invalid amount input

        # Ensure the amount is valid (greater than 0)
        if amount > 0:
            mshwari_account.available_balance += amount  # Increase the available balance
            mshwari_account.save()  # Save the updated account

            messages.success(request, f"Deposit of Ksh {amount} was successful.")
        else:
            messages.error(request, "Deposit failed. Please ensure the amount is valid.")
        
        return redirect('deposit_funds')  # Redirect to the same page to show updated account info

    return render(request, 'mshwari/deposit_funds.html', {'mshwari_account': mshwari_account})


@login_required
def withdraw_funds(request):
    user = request.user
    try:
        # Get the MShwari account for the logged-in user
        mshwari_account = MShwari.objects.get(account__user=user)
    except MShwari.DoesNotExist:
        # If MShwari account does not exist, redirect to create one
        messages.error(request, "MShwari account not found. Please create one.")
        return redirect('create_mshwari_account')

    if request.method == "POST":
        # Get the amount from the form, convert it to Decimal for precision
        amount = Decimal(request.POST.get('amount'))

        # Ensure that the MShwari account has enough available balance
        if mshwari_account.available_balance >= amount:
            # Deduct the amount from the MShwari available balance
            mshwari_account.available_balance -= amount
            mshwari_account.save()

            # Get the user's Mpesa account and add the withdrawn amount
            mpesa_account = Account.objects.get(user=user)
            mpesa_account.balance += amount
            mpesa_account.save()

            messages.success(request, f"Withdrawal of Ksh {amount} was successful.")
        else:
            messages.error(request, "Insufficient balance in MShwari. Withdrawal failed.")

        return redirect('withdraw_funds')  # Redirect to the withdrawal page for updated data

    return render(request, 'mshwari/withdraw_funds.html', {'mshwari_account': mshwari_account})

@login_required
def lock_funds(request):
    user = request.user
    mshwari_account = MShwari.objects.get(account__user=user)
    
    if request.method == "POST":
        amount = float(request.POST.get('amount'))
        lock_end_date = request.POST.get('lock_end_date')
        
        if mshwari_account.lock_savings(amount, request.POST.get('lock_start_date'), lock_end_date):
            messages.success(request, f"Amount of Ksh {amount} successfully locked until {lock_end_date}.")
        else:
            messages.error(request, "Lock savings failed. Please check your balance and try again.")
        
        return redirect('lock_funds')  # Redirect to the same page to show updated account info

    return render(request, 'mshwari/lock_funds.html', {'mshwari_account': mshwari_account})


@login_required
def create_mshwari_account(request):
    user = request.user
    
    # Check if the user already has an MShwari account
    try:
        # Try to get the MShwari account associated with the user's Account
        mshwari_account = MShwari.objects.get(account__user=user)
        return redirect('dashboard')  # Redirect to the MShwari dashboard if account exists
    except MShwari.DoesNotExist:
        # Proceed to create MShwari account if it doesn't exist
        if request.method == 'POST':
            form = MShwariAccountForm(request.POST)
            if form.is_valid():
                # Get the user's Account instance
                account = Account.objects.get(user=user)
                
                # Create the MShwari account and link it to the user's account
                mshwari_account = form.save(commit=False)
                mshwari_account.account = account  # Link the MShwari account to the user's main Account
                mshwari_account.save()
                
                return redirect('dashboard')  # Redirect to the MShwari dashboard after successful creation
        else:
            form = MShwariAccountForm()

        return render(request, 'mshwari/create_mshwari_account.html', {'form': form})