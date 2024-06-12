from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm

#The following are the imports for the PDF file upload and processing
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

from rest_framework.response import Response
from uagents.query import query  # Assuming uagents library is installed
from .models import SummariseRequest, DataMappingRequest, RecommedRequest
from .serializers import SummariseResponseSerializer, DataMappingResponseSerializer, RecommedResponseSerializer

# uAgents addreses
summarise_address = ''
data_mapping_address = ''
recomendation_address = ''

# View to render the frontend app
class FrontendAppView(TemplateView):
    template_name = "index.html"

# Custom 404 view
def custom_404(request, exception):
    try:
        return serve(request, 'index.html', document_root=settings.STATICFILES_DIRS[0])
    except IndexError:
        raise Http404("index.html not found in static files")



# View to upload a PDF file
@csrf_exempt
def upload_pdf_view(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)

        files = UploadFile.objects.filter(user=request.user)
        
        title, extension = os.path.splitext(request.FILES['pdf_file'].name)
        
        for file in files:
            print(file.title)
            print(title)
            if file.title == title:
                return JsonResponse({'errors': 'Title already exists'}, status=409)
        if form.is_valid():
            upload_file = form.save(commit=False)
            #Check if the title already exists otherwise throw error
            upload_file.user = request.user
            upload_file.save()
            return JsonResponse({'message': 'File uploaded successfully'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


# View to delete a PDF file
@csrf_exempt
def delete_file(request): 
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method == 'DELETE':
        try:
            # Load the JSON data from the request body
            data = json.loads(request.body)
            title = data.get('title')
            # Retrieve the file from the database
            file = UploadFile.objects.get(title=title, user=request.user)
            file.delete()
            return JsonResponse({'message': 'File deleted successfully'})
        except UploadFile.DoesNotExist:
            return JsonResponse({'error': 'File not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# View to retrieve the content of a PDF file
@csrf_exempt
def file_content(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    title = request.GET.get('title')
    print(title)
    try:
        # Retrieve the file from the database
        file_obj = UploadFile.objects.get(title=title)
    except UploadFile.DoesNotExist:
        print('File not found')
        # If the file does not exist, return a 404 Not Found response
        return JsonResponse({'error': 'File not found'}, status=404)

    # Open the file for reading in binary mode
    with file_obj.pdf_file.open('rb') as file:
        print("file opened")
        file_path = file_obj.pdf_file.path
        print(file_path)
        # Create an HttpResponse with the content of the file
        response = HttpResponse(file.read(), content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="{file_obj.pdf_file.name}"'
        return response


# View to get PDF file from database
@csrf_exempt
def retrieve_file(title):
    try:
        # Retrieve the file from the database
        file_obj = UploadFile.objects.get(title=title)
        return file_obj
    except UploadFile.DoesNotExist:
        return None
    except Exception as e:
        return str(e)



# View to load the documents to llama loader
@csrf_exempt
def load_documents(pdf_file_path):
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    documents = loader.load_data(file=Path(pdf_file_path))
    return documents


# View to create index
@csrf_exempt
def create_index(documents):
    cohere_api_key = os.getenv('cohere_api_key')
    model = "xlarge"
    temperature = 0.9
    max_tokens = 256
    llm = Cohere(model=model, temperature=temperature, cohere_api_key=cohere_api_key, max_tokens=max_tokens)
    embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key)
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embeddings)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    return index

# View to retrieve query results
@csrf_exempt
def retrieve_query_results(index, user_query):
    #this is the query engine with the required embeddings
    query_engine = index.as_query_engine()
    #this is the context that will be used to generate the response
    query_results = query_engine.retrieve(user_query)
    return query_results



@csrf_exempt
def query_with_cohere(context, query):
    cohere_api_key = os.getenv('cohere_api_key')
    co = cohere.Client(cohere_api_key)
    prompt = f"Context: {context}\nQuery: {query}\nAnswer:"
    response = co.generate(
        model='command-nightly',
        prompt=prompt,
        #test limit
        max_tokens=300,
        #the higher the temprature the more creative the response
        temperature=0.7,
        presence_penalty=0.5,
        num_generations=1,  # Generate multiple responses
        stream=False,  # Disable streaming of response
        truncate='END',  # Truncate input at the end if it exceeds the maximum token length
        k=3,  # Enable top-k sampling with k=50
        p=0.75  # Adjust nucleus sampling parameter
    )
    return response.generations[0].text

## MAIN VIEW TO PROCESS THE PDF FILE ## 
@csrf_exempt
def server_pdf(request):
    print(request)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            user_query = data.get('query')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        file_obj = retrieve_file(title)
        if not file_obj:
            return JsonResponse({'error': 'File not found'}, status=404)

        pdf_file_path = file_obj.pdf_file.path
        #LOAD THE DOCUMENTS
        documents = load_documents(pdf_file_path)
        #CREATE THE INDEX
        index = create_index(documents)
        #RETRIEVE THE QUERY RESULTS
        query_results = retrieve_query_results(index, user_query)
        #GET THE CONTEXT FROM THE LLAMA INDEX
        context_from_llama_index = query_results  
        #QUERY THE COHERE API
        cohere_response = query_with_cohere(context_from_llama_index, user_query)
        #RETURN THE RESPONSE
        return JsonResponse({'cohere_response': cohere_response})
    
    else:
        return HttpResponse('Method not allowed', status=405)


# View to login
@require_POST
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'detail': 'Login successful'})
        else:
            return JsonResponse({'detail': 'Invalid credentials'}, status=400)


# View to check if the user is authenticated
@csrf_exempt
def whoami_view(request):
    print(request.user)
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'username': request.user.username})


# View that gets all the PDF files uploaded by the user
@login_required
def list_files(request):
  if not request.user.is_authenticated:
    return JsonResponse({'error': 'Unauthorized'}, status=401)

  files = UploadFile.objects.filter(user=request.user) # Filter by user
  titles = [file.title for file in files]
  return JsonResponse({'files': titles})


# Register view
@csrf_exempt
def register(request):
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
        return JsonResponse({'status': 'only POST method is allowed'}, status=405)

# Logout view   
@csrf_exempt
def logout_view(request):
        logout(request)
        return JsonResponse({'status': 'success'}, status=200)

@csrf_exempt
async def summarise_information(request):
    response = await query(destination=summarise_address, message=SummariseRequest(), timeout=15.0)
    data = json.loads(response.decode_payload())
    return data
@csrf_exempt
async def map_data(request):
    response = await query(destination=data_mapping_address, message=DataMappingRequest(), timeout=15.0)
    data = json.loads(response.decode_payload())
    return data

@csrf_exempt
async def recommend(request):
    response = await query(destination=recomendation_address, message=RecommedRequest(), timeout=15.0)
    data = json.loads(response.decode_payload())
    return data