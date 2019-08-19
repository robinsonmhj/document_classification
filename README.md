The repo is used for document classification, you can use it locally or deploy it to a public/private cloud
See the Dockerfile for details



How to use it

First build a docker using the docker file
docker build -t document-classification .

Second, run a container 

docker run --rm document-classification -p 80:80

To use the API as webservice, a token is needed. Make sure that you have the token.
BTW, the token is written in the file and you can see it and use it. For product use, it is not encouaged to put the token in the code



