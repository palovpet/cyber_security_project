## Things that annoy me - the unsafe application

__Things that annoy me__ is a place to lighten one's heart by typing what is causing them to be pissed off. 
A user can also view their TOP 3 list of things that have annoyed them, as well as view every annoying thing they have ever recorded. 
Unlike the front page is promising, the application is not safe. It contains five security flaws from the OWASP Top Ten list of 2021.

The application is available in heroku: [click](https://csp-ttam.herokuapp.com/)

(If you are using some other browser than chrome you might need to refresh the heroku-page a few times)

### Security issues in the application

- Flaw 1: CSFR
- Flaw 2: Injection
- Flaw 3: Broken access control
- Flaw 4: Cryptographic Failure
- Flaw 5: Security misconfiguration

The fixes for the issues are in the code as comments, they are also explaned in the report: [click](https://github.com/palovpet/cyber_security_project/blob/master/report.md).


*This project is made for the course Cyber Security Base: Course Project I TKT200093.*
