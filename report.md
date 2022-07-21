# Cyber Security Base: Course Project I

This application is the course project of the Cyber Security Base –course. It contains five security flaws, four of which are from the [OWASP top ten list of 2021](https://owasp.org/www-project-top-ten/) and one is CSFR. 

### Installing and running the web application

The application is coded using Python and Flask, and to make running it easier it is available in heroku: [click](https://csp-ttam.herokuapp.com/). The testing has been done using 
chrome and that is the browser it performs most optimally with. When using some other browser I noticed sometimes needing to 
refresh the pages again to get them working. 

Source code is available in github: [click](https://github.com/palovpet/cyber_security_project)

To test the application there are two test users, but it is possible to also create a new (non-admin) user.

__Test user__


```
username: tester

password: tester
```

__Admin test user__


```
username: admintester

password: admintester
```

# Security flaws in the application

When possible the fixes to the issues are also in the source code, but explaned in more detail below.

## 1: Cross-site Request Forgery (CSFR)

### Flaw:

The application does not contain checks that the requests are coming from the actual user, this makes it 
possible for the hijacker to act as the user in the application. 

These methods don't contain a CSFR-check:

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/routes.py#L52

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/routes.py#L68

### Fix:
To fix the flaw a CSFR token should be attached to the user, and each form and the method handling the form
should contain a validation that the token is correct

Attach CSFR-token to a user when logging in:

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/users.py#L21

Add method for checking the CSFR-token and aborting if it doesn't match:

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/users.py#L80

Add CSFR-check to the methods listed above:

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/routes.py#L56

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/routes.py#L71

Save the CSFR-token of the one accessing the forms to check it with the method above:

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/templates/index.html#L26

https://github.com/palovpet/cyber_security_project/blob/4c9e56ce047fd334e71837e45c39661c83bed972/templates/mythings.html#L23

## 2: Injection
### Flaw:

This vulnerability makes it possible for the user to query the database for orher information than for what 
the user is intended to searh. To test this log in and click the link after sentence "Things that have previously annoyed you"
to access TOP 3 list on page /mythings. In the "Name of thing" -field you can for example get the admin passwords with typing:

```
x' and 1=1 UNION SELECT password FROM endusers WHERE admin = 1 or username like 'xxx
```

The issue is with the badly parametrizied method:

https://github.com/palovpet/cyber_security_project/blob/4c9e56ce047fd334e71837e45c39661c83bed972/things.py#L45

### Fix:

To fix the issue, the query to database should have better parametrization:

https://github.com/palovpet/cyber_security_project/blob/4c9e56ce047fd334e71837e45c39661c83bed972/things.py#L49

## 3: Broken access control
### Flaw:

Application contains a flaw that makes it possible to view anyone's list of things that have annoyed them
only with knowing their username. Obviously these kinds of lists should be personal, and the application should contain 
a check to see if a user is allowed to view the information they are trying to access. To try this you can view Seppo's 
list with the ULR:

```
https://csp-ttam.herokuapp.com/allmythings/seppo
```

Issue is with this handler method:

https://github.com/palovpet/cyber_security_project/blob/4c9e56ce047fd334e71837e45c39661c83bed972/routes.py#L43

### Fix:

To fix the issue, application should contain checks that the user trying to access certain page is allowed to view the information.

Add a method for validating the user is accessing their own information:

https://github.com/palovpet/cyber_security_project/blob/4c9e56ce047fd334e71837e45c39661c83bed972/users.py#L69

Use the method to check the person is allowed to view the information or re-route a hacker to error-page:

https://github.com/palovpet/cyber_security_project/blob/4c9e56ce047fd334e71837e45c39661c83bed972/routes.py#L46

## 4: Cryptographic Failure
### Flaw:
The passwords are saved to the database as regular text, thus making the users very voulnerable if an attacker would 
gain access to the database, for example with the SQL Injection described previously.

The signin-method saves passwords as regular text:

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/users.py#L30

And login-method compares the regular text password:

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/users.py#L6


### Fix:
A good way to save passwords safer is to store a hash value of the passwords. As we know, this doesn't make hacking into
 someones account impossible, but it will surely slow the attacker.
 
Edit the users.py class methods to save and check passwords as hashed, utilize werkzeug.security utility:

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/users.py#L3

Make changes to both signin-method

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/users.py#L41

and login-method

https://github.com/palovpet/cyber_security_project/blob/44793c2a43db96cdb6cf2c0d720af84cee5edf8b/users.py#L14

## 5: Security misconfiguration
### Flaw:
The developer of this application has done thorough production testing in heroku, and created a admin test user for
this purpose. Unfortunately she used very guessable username and password, and left the test user active after launching
 the application. As admins can view everything anyone has ever saved, if someone would guess the user and password 
 (or get them with the SQL injection) they'd see everything. The tempting link for admin stuff is also left to the index.html 
 to get a hacker curious. 
 
 The tempting link:
  
 https://github.com/palovpet/cyber_security_project/blob/4c9e56ce047fd334e71837e45c39661c83bed972/templates/index.html#L32
  
### Fix:
To fix the issue the tempting link should be deleted, as it doesn't really serve a purpose in the application. When logged in the admin could still view
 the admin.html by typing the URL. Obviously the developer should have also deleted or deactivated the admin test user after releasing the application, and
  if admin user is needed the username and password should be something more secure than *admintester*.
