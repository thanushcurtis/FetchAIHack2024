# Template for Computer Science BSc Final Year Project.

## Local development

## Prerequisite
1. Inorder to avoid dependency overlaps it is adivceable 
install conda and create a environment using the code:

    ```console
        conda create -n myenv python=3.10
    ```
2. Activate the conda environment
    ```console
       conda activate myenv
    ```

## Next:

1. Install Pyhton dependencies (main folder):

    ```console
    $ pip install -r requirements.txt
    ```
## Method 1

2. Windows; 

     ```console
    $ waitress-serve --listen=127.0.0.1:8080 project.wsgi:application

    ```
3. Now simple go to:
      
      http://127.0.0.1:8080


## And/Or 

2. MacOS & Linux Operating Sytems can run:

  ```console

    $ python app.py

    ```

## Method 2
2. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    ```




