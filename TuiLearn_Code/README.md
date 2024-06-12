# Template for Computer Science BSc Final Year Project.

## Local development

## Prerequisite
1. Inorder to avoid dependency overlaps it is adivceable 
install conda at: https://docs.anaconda.com/free/miniconda/ and go to miniconda promt.
create a environment using the code:

    ```console
        conda create -n myenv python=3.10
    ```
2. Activate the conda environment
    ```console
       conda activate myenv
    ```

## Next:

1. Install Pyhton dependencies (main folder - this might take some time):

    ```console
    $ pip install -r requirements.txt
    ```
## Method 1

2. Windows; 

     ```console
    $ waitress-serve --listen=127.0.0.1:8080 project.wsgi:application

    ```
3. Now simply go to:
      
      http://127.0.0.1:8080


## And/Or 

2. MacOS & Linux Operating Sytems can run:

  ```console

    $ python app.py

    ```
3. Now simply go to:
      
      http://127.0.0.1:8080



## Method 2
2. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    
    ```

## In case of api error
Just for deveplopment and testing!!

Please set the api key in the /api/view.py on lines 141 & 164:

'xheV3bxCvQh4yf68TblDCHHsMlAyBS00Ii6Ya8y7'


