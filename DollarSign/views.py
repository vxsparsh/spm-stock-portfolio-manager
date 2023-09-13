import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .forms import StockForm, RegistrationForm
from django.core.cache import cache
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#  IEX Cloud API token
IEX_API_TOKEN = 'pk_2d82d25a62ac4a4fb95d293e6f9c84e6'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def home(request):
    if request.method == 'POST':
        stock_ticker = request.POST['stock_ticker']
        stocks = search_stock(stock_ticker)
        return render(request, 'home.html', {'stocks': stocks})
    return render(request, 'home.html')

@login_required
def about(request):
    return render(request, 'about.html')

def search_stock(stock_ticker):
    try:
        #API URL
        url = f'https://cloud.iexapis.com/stable/stock/{stock_ticker}/quote?token={IEX_API_TOKEN}'
        
        # Send a GET request to the IEX Cloud API
        response = requests.get(url)
        data = response.json()
        
        if 'symbol' in data:
            return data
        else:
            return {'Error': 'There was a problem with your provided ticker symbol. Please try again'}
    except Exception as e:
        return {'Error': 'There has been some connection error. Please try again later.'}

@login_required
def check_valid_stock_ticker(stock_ticker):
    stock = search_stock(stock_ticker)
    if 'Error' not in stock:
        return True
    return False

@login_required
def check_stock_ticker_existed(stock_ticker):
    try:
        stock = Stock.objects.get(ticker=stock_ticker, user=request.user)
        if stock:
            return True
    except Exception:
        return False

@login_required
def portfolio(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock_ticker = form.cleaned_data['ticker']
            stock_info = fetch_stock_info(stock_ticker)
            
            if stock_info:
                stock = form.save(commit=False)
                stock.purchase_date = form.cleaned_data['purchase_date']
                stock.latestPrice = stock_info.get('latestPrice', 0.0)
                stock.previousClose = stock_info.get('previousClose', 0.0)
                stock.marketCap = stock_info.get('marketCap', 0.0)
                stock.returnYTD = stock_info.get('ytdChange', 0.0)
                stock.peRatio = stock_info.get('peRatio', 0.0)
                stock.week52High = stock_info.get('week52High', 0.0)
                stock.week52Low = stock_info.get('week52Low', 0.0)
                stock.current_value = stock.latestPrice * stock.shares
                stock.symbol = stock_info.get('symbol', 'N/A')
                stock.companyName = stock_info.get('companyName', 'N/A')
                stock.user = request.user  # Associate the stock with the logged-in user
                stock.save()  # Save the updated stock data
                messages.success(request, f'{stock.ticker} has been added successfully.')
            else:
                messages.warning(request, f"Ticker {stock_ticker} does not exist.")
        else:
            messages.warning(request, 'Please correct the form errors.')

    stockdata = Stock.objects.filter(user=request.user)
    total_portfolio_value = 0

    for stock in stockdata:
        stock_info = fetch_stock_info(stock.ticker)
        if stock_info:
            stock.latestPrice = stock_info.get('latestPrice', 0.0)
            stock.previousClose = stock_info.get('previousClose', 0.0)
            stock.marketCap = stock_info.get('marketCap', 0.0)
            stock.returnYTD = stock_info.get('ytdChange', 0.0)
            stock.peRatio = stock_info.get('peRatio', 0.0)
            stock.week52High = stock_info.get('week52High', 0.0)
            stock.week52Low = stock_info.get('week52Low', 0.0)
            stock.current_value = stock.latestPrice * stock.shares
            stock.symbol = stock_info.get('symbol', 'N/A')
            stock.companyName = stock_info.get('companyName', 'N/A')
            stock.save()  # Save the updated stock data
            total_portfolio_value += stock.current_value
        else:
            # Handle the case where stock_info is None
            messages.warning(request, f"Unable to fetch data for {stock.ticker}.")
            stock.latestPrice = 0.0
            stock.previousClose = 0.0
            stock.marketCap = 0.0
            stock.returnYTD = 0.0
            stock.peRatio = 0.0
            stock.week52High = 0.0
            stock.week52Low = 0.0
            stock.current_value = 0.0
            stock.symbol = 'N/A'
            stock.companyName = 'N/A'

    return render(request, 'portfolio.html', {'stockdata': stockdata, 'total_portfolio_value': total_portfolio_value})

# Cache stock data fetching
def fetch_stock_info(stock_ticker):
    cache_key = f'stock_info_{stock_ticker}'
    stock_info = cache.get(cache_key)
    if stock_info is None:
        # If not in cache, fetch from the API
        stock_info = search_stock(stock_ticker)
        # Cache the data for a reasonable duration (e.g., 1 hour)
        cache.set(cache_key, stock_info, 3600)
    return stock_info

@login_required
def delete_stock(request, stock_symbol):
    stock = Stock.objects.get(ticker=stock_symbol, user=request.user)
    stock.delete()
    messages.success(request, f'{stock.ticker} has been deleted successfully.')
    return redirect('portfolio')

@login_required
def store_data_in_session(request):
    # Store user-specific data in sessions
    request.session['user_id'] = request.user.id
    request.session['username'] = request.user.username
    
    return HttpResponse("Data stored in session.")

@login_required
def retrieve_data_from_session(request):
    # Retrieve user-specific data from sessions
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    
    if user_id and username:
        return HttpResponse(f"User ID: {user_id}, Username: {username}")
    else:
        return HttpResponse("User-specific data not found in session.")
