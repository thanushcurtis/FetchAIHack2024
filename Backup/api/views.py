from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm

"""
The following are the imports for the PDF file 
upload and processing
"""

from .models import UploadFile
import json
import cohere
from llama_index import ServiceContext, VectorStoreIndex
from pathlib import Path
from llama_index import download_loader
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.llms.cohere import Cohere
from .forms import UploadPDFForm
import os

from django.views.generic import TemplateView
from django.http import Http404
from django.conf import settings
from django.views.static import serve

"""These are the addresses for the agents"""
summarise_address = ''
data_mapping_address = ''
recomendation_address = ''

class FrontendAppView(TemplateView):
    """
    This view renders the frontend app

    Attributes:
    template_name : str
    """

    template_name = "index.html"

def custom_404(request, exception):
    """This view handles 404 errors"""

    try:
        return serve(request, 'index.html', 
                     document_root=settings.STATICFILES_DIRS[0])
    except IndexError:
        raise Http404("index.html not found in static files")

# View to upload a PDF file
@csrf_exempt
def upload_pdf_view(request):
    """
    This view uploads the pdf files
    
    Attributes:
    form : gets the form for uploading file
    files : gets the file object
    title, extension : used for accessing file
    upload_file : saves the file from the form
    """
    
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)

        files = UploadFile.objects.filter(user=request.user)
        
        title, extension = os.path.splitext(request.FILES['pdf_file'].name)
        
        for file in files:
            print(file.title)
            print(title)
            if file.title == title:
                return JsonResponse({'errors': 'Title already exists'}, 
                                    status=409)
        if form.is_valid():
            upload_file = form.save(commit=False)

            """Check if the title already exists otherwise throw error"""
            upload_file.user = request.user
            upload_file.save()
            return JsonResponse({'message': 'File uploaded successfully'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt
def retrieve_file(title):
    """
    This view gets the PDF files from the database

    Attributes:
    file_obj : stores the file object
    """
    try:
        file_obj = UploadFile.objects.get(title=title)
        return file_obj
    except UploadFile.DoesNotExist:
        return None
    except Exception as e:
        return str(e)

@csrf_exempt
def load_documents(pdf_file_path):
    """
    This view loads the documents to llama loader 
    """

    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    documents = loader.load_data(file=Path(pdf_file_path))
    return documents

@csrf_exempt
def create_index(documents):
    """
    This view creates indexes
    """

    cohere_api_key = os.getenv('cohere_api_key')
    model = "xlarge"
    temperature = 0.9
    max_tokens = 256
    llm = Cohere(model=model, temperature=temperature, 
                 cohere_api_key=cohere_api_key, max_tokens=max_tokens)
    embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key)
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embeddings)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    return index

@csrf_exempt
def retrieve_query_results(index, user_query):
    """
    This view gets the query results
    """

    query_engine = index.as_query_engine()
    query_results = query_engine.retrieve(user_query)
    return query_results

@csrf_exempt
def query_with_cohere(context, query):
    """
    This view sends the query to cohere and returns the response
    """

    cohere_api_key = os.getenv('cohere_api_key')
    co = cohere.Client(cohere_api_key)
    prompt = f"Context: {context}\nQuery: {query}\nAnswer:"
    response = co.generate(
        model='command-nightly',
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
        presence_penalty=0.5,
        num_generations=1,  
        stream=False, 
        truncate='END',  
        k=3,  
        p=0.75  
    )
    return response.generations[0].text

@csrf_exempt
def server_pdf(request):
    """
    This view processes the PDF files
    """

    print(request)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = "IBP"
            user_query = data.get('query')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, 
                                status=400)

        file_obj = retrieve_file(title)
        if not file_obj:
            return JsonResponse({'error': 'File not found'}, 
                                status=404)

        pdf_file_path = file_obj.pdf_file.path
        documents = load_documents(pdf_file_path)
        index = create_index(documents)
        query_results = retrieve_query_results(index, user_query)
        context_from_llama_index = query_results  
        cohere_response = query_with_cohere(context_from_llama_index, 
                                            user_query)
        return JsonResponse({'cohere_response': cohere_response})
    
    else:
        return HttpResponse('Method not allowed', status=405)

@require_POST
@csrf_exempt
def login_view(request):
    """
    This view allows the user to log in
    """

    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, 
                            password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'detail': 'Login successful'})
        else:
            return JsonResponse({'detail': 'Invalid credentials'}, s
                                tatus = 400)

@csrf_exempt
def whoami_view(request):
    """
    This view checks if the user is authenticated
    """

    print(request.user)
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'username': request.user.username})

@login_required
def list_files(request):
  """
  This view gets all the PDF files uploaded by the user
  """

  if not request.user.is_authenticated:
    return JsonResponse({'error': 'Unauthorized'}, status=401)

  files = UploadFile.objects.filter(user = request.user) 
  titles = [file.title for file in files]
  return JsonResponse({'files': titles})

@csrf_exempt
def register(request):
    """
    This view allows the user to register
    """

    if request.method == "POST":
        print(request.POST)
        # Load the JSON data 
        data = json.loads(request.body)
        form = RegisterForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'only POST method is allowed'}, 
                            status=405)

# Logout view   
@csrf_exempt
def logout_view(request):
        """
        This view allows the user to log out
        """

        logout(request)
        return JsonResponse({'status': 'success'}, status=200)