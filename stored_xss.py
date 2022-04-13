from ast import arg
import imp
import requests;
from requests.models import Response;
import argparse;
import os;

parser= argparse.ArgumentParser(description="Stored XSS automation script");
parser.add_argument('-u', required= True, help="database username" );
parser.add_argument('-p', required=True, help="database password");
parser.add_argument('-url', required=True, help="URL of the application" );
args = parser.parse_args();

def runMysql_Command(username, password, url):
    print(username, password, url);
    os.system(f"mysql -u {username} -h pravin.itechers.net --password='{password}' -e 'select * from itecher.staff'");
    


username    = args.u;
password    = args.p;
url         = args.url;
runMysql_Command(username,password,url);

