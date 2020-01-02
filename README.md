# Bank model

This is a Bank simulation implemented as a Restful API that supports everday banking features like opening an account with a unique username and password, depositing money in your account, transferring money into another account, checking balance and taking and paying loan from and to the bank. Each tranaction costs the user $1 which is simulated by transfer of $1 from user's account to bank's account.Taking loan increases user's amount and the debt while paying back lone does the opposite. With each query, a message and a status code is returned. A message tells the user if his transaction is successfull or there is anything invalid. The status code is another way of stating the traction success. 200 denotes success, 301 denotes invalid user, etc.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
Python3, flask
MongoDB
Docker, Docker-compose
Postman
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Python : 
https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html 
Flask:
https://pypi.org/project/Flask/ 
MongoDB :
https://docs.mongodb.com/manual/installation/
Docker 
https://docs.docker.com/docker-for-mac/install/ 
Docker-compose 
https://docs.docker.com/compose/install/. 
Postman:
https://www.getpostman.com/downloads/ 

```

### Resource Chart Protocol

```
| Resource      |      URL      | Protocol   | Parameters                                    | status codes
| ------------- | ------------- | ---------  | -------------                                 | ------------- 
| Register      | /register     | POST       | username, password                            | 200 OK, 301 user exists
| Add           | /add          | POST       | username, password, amount                    | 200 OK, 301 invalid user, 302 invalid password, 304 negative amount
| Transfer      | /transfer     | POST       | username, password, amt, receiver's username  | 200 OK, 301 invalid user, 302 invalid password, 304 negative amount, 303 not enough moeny in account
| Check         | /check        | POST       | username, password                            | 200 OK, 301 invalid user, 302 invalid password
| Take loan     | /takeloan     | POST       | username, password, amount                    | 200 OK, 301 invalid user, 302 invalid password
| Pay loan      | /payloan      | POST       | username, password, amount                    | 200 OK, 301 invalid user, 302 invalid password, 303 not enough moeny in account, 304 negative amount

```



## Running the tests
"
In your local machine, go to your project directory and run
 * sudo docker-compose build <br />
 * sudo docker-compose up <br />
 Once the API is running, copy the host url and paste it in post man, and give your command after /. In postman, <br />
 * create an account using a username and password on a POST protocol with /register URL <br />
 * add money to your account using your username, password and a non-negative amount on a POST protocol with /add URL <br />
 * check balance of your account using username, password on a POST protocol with /check URL <br />
 * Take loan from bank using username, password and an amount on a POST protocol with /takeloan URL <br />
 * Pay back loan to the bank using username, password and an amount on a POST protocol with /takeloan URL <br />

 
 **Registration** <br />
<img width="412" height="350" alt="Screen Shot 2020-01-02 at 12 26 59 AM" src="https://user-images.githubusercontent.com/41305591/71652979-dfb5cf80-2cf7-11ea-9038-a5cc4de26216.png"> <br />
 **Depositing money** <br />
<img width="455" height="350" alt="Screen Shot 2020-01-02 at 12 27 32 AM" src="https://user-images.githubusercontent.com/41305591/71653002-0a078d00-2cf8-11ea-9ab6-c3a7717254fd.png"> <br />

 **Transfer Money** <br />
  <img width="442" height="350" alt="Screen Shot 2020-01-02 at 12 42 35 AM" src="https://user-images.githubusercontent.com/41305591/71653151-de38d700-2cf8-11ea-9782-d057d45ef414.png"><br />
 
  **Check balance** <br />
 <img width="326" alt="Screen Shot 2020-01-02 at 12 28 28 AM" src="https://user-images.githubusercontent.com/41305591/71653043-581c9080-2cf8-11ea-8c64-40bd93e8df41.png"> <br />
 
 **Take loan** <br />
 <img width="379" alt="Screen Shot 2020-01-02 at 12 28 02 AM" src="https://user-images.githubusercontent.com/41305591/71653169-00325980-2cf9-11ea-9d8c-d7ec84bee333.png"> <br />
 
  **Pay loan** <br />
  <img width="387" alt="Screen Shot 2020-01-02 at 12 32 54 AM" src="https://user-images.githubusercontent.com/41305591/71653203-3cfe5080-2cf9-11ea-92d4-c748404ba674.png"> <br />
 
 
 ## Running edge test cases ##
 **Registering a user twice** <br />
  <img width="363" height="350" alt="Screen Shot 2020-01-02 at 12 49 26 AM" src="https://user-images.githubusercontent.com/41305591/71653435-5eac0780-2cfa-11ea-8932-60291d369c4d.png"> <br />
 
 **Invalid user** <br />
 <img width="325" height="350" alt="Screen Shot 2020-01-02 at 12 57 04 AM" src="https://user-images.githubusercontent.com/41305591/71653536-e2fe8a80-2cfa-11ea-8250-a1d699dac49b.png"><br />
 
 **Invalid password** <br />
 <img width="349" alt="Screen Shot 2020-01-02 at 12 49 54 AM" src="https://user-images.githubusercontent.com/41305591/71653469-9d41c200-2cfa-11ea-908f-8cebb09a0a9d.png"> <br />
 
 **Not enough amount** <br />>
<img width="395" height="350" alt="Screen Shot 2020-01-02 at 12 51 49 AM" src="https://user-images.githubusercontent.com/41305591/71653629-7f289180-2cfb-11ea-877b-8fadfbc98c44.png"><br />

 **Entering a negative amount** <br />>
 <img width="696" height="350" alt="Screen Shot 2020-01-02 at 12 51 20 AM" src="https://user-images.githubusercontent.com/41305591/71653667-bac35b80-2cfb-11ea-8a4d-bc453942092d.png">

 

## Deployment

Create a EC2 instance in AWS console, download the pep file and run the following commands:  <br />
* ssh -i "Pem file location""pem file name".pem.txt "username"@"public dns of your instance"  <br />
 install docker and docker-compose.  <br />
* mkdir "directory name"  <br />
* cd "directory name"
* git clone "your git link to the application containing docker-compose.yml"  <br />
* sudo docker-compose build <br />
* sudo docker-compose up. <br />
 
 Your application should now be up and running on AWS
 
## Acknowledgments

* Udemy
* El Farouk Yaseer
