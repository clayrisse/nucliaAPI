python -m pip install python-dotenv



#Objective
Create a script that would read a local folder and upload to Nuclia all the PDF files it
contains, and then create a static web page allowing users to search into these files.

##Guidelines and recommendations
- You can use the programming language you want. If you choose Python or JS/TS,
using the existing Nuclia SDKs is not a requirement, you are free to use them if you
want to, but making direct calls to the API is absolutely fine.
- Push your code to a public GitHub repository. The README page will explain how to
install and run the script.
- Put the search page on GitHub Pages.
- You will have to create your own Nuclia account on https://nuclia.cloud and make
your knowledge box public.
- You can use all the information provided at https://docs.nuclia.dev/ and you can ask
questions on the Nuclia Discord public channels.


> Bonus 1:
> Make sure the script does not make duplicates if we import the same files twice

> Bonus 2:
> Make your knowledge box private and create an HTTP service that would proxy calls
> to Nuclia and add automatically the needed HTTP headers so anonymous users can
> search in your private knowledge box (Note: deployment of such proxy is
> out-of-scope).

Implement a proxy layer
Tagging the resources
Imagine that you want to restrict access to a set of resources in a Knowledge Box according the group the current user belongs to.

You will store the authorized groups as a keywordset field in each resource at the time it is created. The resource creation payload will look like:
```sh
{
"title": "Meeting minutes",
"texts": { "text": { "format": "PLAIN", "body": "some random text" } },
"keywordsets": {
"groups": { "keywords": [{ "value": "group1" }, { "value": "group2" }] }
}
}
```
The groups key here is just an example. It can be anything you base your access restriction on: usernames, etc. Just use a relevant key to store the values.

Adding a filter to requests
Whenever your application needs to query Nuclia to run a search, you will have to add the groups filter to the request in order to make sure you will retrieve only the resources that are authorized to the current user.

For example, assuming the current user belongs to group2, a query like:

```sh
/search?query=secret+information
```

Needs to be modified to:

```sh
/search?query=secret+information&filters=f/groups/group2
```

The extra filters parameter here will select the resources where the groups keywordset contains group2.


##Observations
Thingd to fix:in the documentation page:

1. Python script to upload folder setting labels has 2 quote maks in KNOWLEDGE_BOX
2. Change npm install npm install @nuclia/sdk rxjs to npm i @nuclia/core in JDK guide??