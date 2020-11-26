This document offer a [documentation of the api](#api_documentation) used in the Ponzi project.
In this document you will also find [how the paswords are hashed  ](#hash)

 <a name="api_documentation"></a>
# Rest Api Documentation
## Loging
Most of the requests need a token in order to be able to identify the person. This section present the way of creating one and getting it.

### Registering
Before doing anything you need to register into the system. To register, use this url :

``PUT http://127.0.0.1:5002/login``

This url take two query parameters, the "username" and the "hash" of the password. 
It also takes a third parameter which is an "invited_by", the invite code of the person who invited this new person.
All of those parameters are mandatory. Any request without the three of them will receive a 400 error code
If the username is already taken, you will receive a 403 error code.
If the username is not already taken, the account will be created in the database, associated with a *invite_code* (used to invite other persons) and with a *token* used to authenticate. This url returns a dictionary under this form : 
{token = "azertyuio"}
Here is an example of how you would use the registering : 

`PUT http://127.0.0.1:5002/login?username=yourusername&hash=yourhash&invited_by=5434567898`

### Login
You want to do this phase only if you do not already have the token of your user. To login use this url : 

``GET http://127.0.0.1:5002/login``

It takes two query parameters, the username and the hash of the password. If the loging informations are correct you will receive the token under this form : {token = "azertyuio"}. It the loging informations are incorect you will receive a 403 error code.
## Token
**For all the following requests you will need to add a header whose name is "Authentication" and value is the token of your user.**
##Inviting Friends
The goal of a Ponzi Pyramidal model is to invite as much person as possible. The more you invite persons, the more you gain. Thus we need a way of knowing which person was invited by who and distribute the money created by this invitation. 
###Getting Invite Code
You can get the invite code of a user by using this url : 

``GET http://127.0.0.1:5002/invite``

You will find the invitation code in a field named "*invite_code*" in the response.

 <a name="hash"></a>
 
## Money

The more people come into the system, the more money is generated. We need to offer a way for users to get the money they won by inviting other people. We also need to give a way to the user to know his balance.

### Balance

You can get the current balance of a user via this url : 

`GET http://127.0.0.1:5002/money`

The current balance of the user will be find in the *balance* field.

### Retrieving money

The user can retrieve his money via this url : 
`GET http://127.0.0.1:5002/money`

The difference between this and the balance is that this one take a query parameter called *amount* which take as value the number of money the user cant to retrieve.

If the value of the *amount* parameter is greater than the balance of the user, all the money of the user will be retrieved.

As a confirmation, is send back in the response, the amount of money the user retrieved in the field *amount* **in** the response.

# Hashing  passwords

The password hashing process uses the *Password-Based Key Derivation Function 2* (or *PBKDF2*) derivation function.
It uses the sha256 encoding. The text to encrypt is the password and the salt is t username both encoded in utf-8. The *PBKDF2* iterates 1 000 000 times.
With this operation we convert a password and a username into a bytestring (or Array of Bytes), in order to send it to the server via the rest api (because all of this work is done in the client), we need to transform it into letters and numbers. The best algorithm for this is the base64 algorithm. We apply this one to the bytestring and obtain a bytestring that we can easely convert into a string. It is then ready to be send via the "hash" field in the rest api.


