## Pension Recommendation

#Description of project
This pension recommendation system enables insurance providers to upload client documents (such as name, age, and employment details) to accurately assess the potential pension entitlements for clients based on a specific pension scheme.

#Instructions to run project

#Prerequisite
1) To avoid dependency overlaps, create a virtual environment
```conda create -n myenv python=3.10```
3) Activate the environment
```conda activate myenv```

#To run the program
1) Navigate into the Backup folder
2) Run the following command
'''pip install -r requirements.txt'''

3) To run the project, run the following command
'''waitress-serve --listen=127.0.0.1:8080 project.wsgi:application'''

#Use-case example

Here we have an example of a document containing details of a pension scheme (this can be in any format):

Here we have an example of a document containing client details (this can take any format):

The user uploads the client details:

The program then recommends pension entiltlment for every client based on the pension scheme, and explains why this is the calculated value:

#Special considerations
