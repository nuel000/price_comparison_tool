from concurrent.futures import ThreadPoolExecutor
from django.shortcuts import render
from .forms import SearchForm
from scrappers.ebay import run_playwright as ebay_run_playwright
from scrappers.walmart import run_playwright as walmart_run_playwright



def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        try:
            if form.is_valid():
                keyword = form.cleaned_data['keyword']

                with ThreadPoolExecutor(max_workers=2) as executor:
                    ebay_future = executor.submit(ebay_run_playwright, keyword)
                    walmart_future = executor.submit(walmart_run_playwright, keyword)

                # Get the results from both futures
                try:
                    ebay_results = ebay_future.result()
                    # print('EBBAYYYY:::::::::::::;',ebay_results)
                except Exception as ebay_error:
                    ebay_results = 'No Results from Ebay'

                try:
                    walmart_results = walmart_future.result()
                    # print('WALMART:::::::::::::;',walmart_results)
                except Exception as walmart_error:
                    walmart_results = 'No results from walmart'

                return render(request, 'search.html', {'form': form, 'ebay_results': ebay_results, 'walmart_results': walmart_results})

        except Exception as e:
   
            return render(request, 'error.html', {'form': form, 'error_message': str(e)})

    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})
