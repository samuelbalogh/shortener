# URL shortener POC


This is a URL shortener proof-of-concept.

## Details

### Usage

To try the "production" version deployed on Heroku, run `make prodpost`. This will post a URL (with `curl`) to the app and it should return a short URL. Visiting the short URL should redirect to the original one:

> NOTE: the Heroku dyno might be in a sleeping state, so the first request might take a few seconds.

```
make prodpost
Posting https://xkcd.com/1313 to the shortener service..
The resulting short URL:
https://urlshrtr.herokuapp.com/2
```

```
 curl https://urlshrtr.herokuapp.com/2
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="b'https://xkcd.com/1313'">b'https://xkcd.com/1313'</a>.  If not click the link.
```

### Running it locally

Python3 is required for the code to run.

To install the dependencies:

```
make install
```

```
make run
```


```
make post
Posting https://xkcd.com/814 to the shortener service..
The resulting short URL:
http://127.0.0.1:5000/1
```


### Implementation

- **Language**: Python
- **Web framework**: Flask
- **Data store**: Redis
- **Cloud platform**: Heroku


### Shortcomings


#### code-related

Things related to the code that would be essential in a production setting:

- **Testing** is only for the happy path - edge cases should be tested
- **Logging** is minimal. More verbose logging would be beneficial.
- **Exception handling** is lacking - error handling is not very thorough.


#### infra-related

Things related to the deployment of the service:

- **load balancing** - such a service must have multiple replicas behind a load balancer in production.
- **monitoring** - request rate, error rate, request latency, Redis memory usage would be some aspects which would have to be monitored
- **rate limiting** would be nice (based on user agent, IP, or other fingerprints)
- **log aggregation** would be nice to have 
