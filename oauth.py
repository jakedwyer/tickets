import oauth2 as oauth
import oauth2.clients.imap as imaplib


clientID = "955724022201.apps.googleusercontent.com";
clientSecret = "uSo45SZzjwRurVOCYekgUSYW";

auth_endpoint= "https://accounts.google.com/o/oauth2/auth"

token_request_uri = "https://accounts.google.com/o/oauth2/auth"
response_type = "code"
client_id = '955724022201.apps.googleusercontent.com'
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
scope = "https://www.googleapis.com/auth/userinfo.profile+https://www.googleapis.com/auth/userinfo.email"

url = token_request_uri + '?response_type=' + response_type + '&client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&scope=' + scope
print url

        
client = oauth.Client(consumer)
print client



resp, content = client.request(TokenEndpoint, "GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])

request_token = dict(urlparse.parse_qsl(content))

print "Request Token:"
print "    - oauth_token        = %s" % request_token['oauth_token']
print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
print 

#List<string> scope = new List<string> 
 #   { 
 #       GoogleScope.ImapAndSmtp.Name,
 #       GoogleScope.EmailAddressScope.Name 
 #   };
