# SpotifyInternshipNotifier
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

Simple Azure Function which notifies you once Spotify posted a new internship offer.
## Features

- Checks Spotify job website for internship offers twice a day and sends you an email containing the current status.
- Uses Azure Functions with Python and the v2 programming model.


## Deployment
1. Create an Azure Function App (either directly in the Azure Portal or via terraform)
2. Create an Azure Communication Service including an Email Communication Service Domain.
3. Add an MailFrom Adress to your Email Communication Service Domain, for example `DoNotReply@<your-domain>.azurecomm.net`
3. In the configuration of your function app, define the following application settings:
   - `MAILING_LIST`: The emails of who will be notified once a new internship is posted, seperated by a `,`. Example: user1@gmail.com,user2@gmail.com
   - `INTERNAL_MAILING_LIST`: The emails who will be notified twice a day on the status of posted internship, i.e. they also receive an email if no new internship was posted. Uses the same format as MAILING_LIST 
   - `SENDER_EMAIL`: The MailFrom Adress you created in Step 3
4. Deploy the function to your function app. You can do this multiple ways:
   - A very simple way is to deploy it via Github Actions, which you can directly integrate with your Azure Function App while creating it in the Azure portal
   - You can also deploy it from your local machine, which I will explain in [this section](#Publish your function to your Azure Function App from your local machine)

## Development
If you want to further adapt this project, you are very welcome to do so. 

### Local testing of Azure Functions
See [this website](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-local) if you want to test your function locally.

### Publish your function to your Azure function app from your local machine
1. Create the function app that you want to deploy your functions to in Azure.
2. Log in to Azure from your command line:
    ```bash
    az login
    ```
3. Publish your code to your function app:
    ```bash
   func azure functionapp publish <name-of-your-functionapp>
    ```

### Debugging Azure functions
Sometimes I find Azure Functions very complicated to debug. A part of this is that when there is something wrong with your functions, 
Azure will still deploy it successfully, but then they simply won't appear in the portal. 

So far I haven't found any way to receive feedback on what went wrong in these cases, so I can only speculate. To help you debug 
these cases faster, here is a list of common bugs that caused my functions to not appear in the portal:

- Not working imports (e.g., because the name of the file changed, or I still used the ".package_name" addressing scheme from the v1 programming model)
- Using the functions' decorators in a wrong way, for example one time I tried to add an `@app.route(...)`decorator to a timer function (which doesn't make any sense ...)
- Forgetting to include dependencies in requirements.txt
- Generally any kind of spelling mistakes, e.g. `@app.function_nam` instead of `@app.function_name`

Also, on another note: if you know a way to get some kind of feedback on what went wrong in these cases, I would love it if you could tell me. Would save me an awful amount of time and nerves ;-).


