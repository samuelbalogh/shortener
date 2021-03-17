# URL shortener POC


This is a URL shortener proof-of-concept.

## Details

### Usage

To try the "production" version deployed on Heroku, run `make prodpost`. This will post a URL (with `curl`) to the app and it should return a short URL. Visiting the short URL should redirect to the original one:

```
Posting https://xkcd.com/1313 to the shortener service..
The resulting short URL:
https://urlshrtr.herokuapp.com/2
```

```
 🍰   curl https://urlshrtr.herokuapp.com/2
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
```


### Implementation

- **Language**: Python
- **Web framework**: Flask
- **Data store**: Redis
- **Cloud platform**: Heroku


### Shortcomings

Things that a production 

- Testing is only for the happy path
- Logging is minimal
- Exception handling is lacking
- Rate limiting would be nice to have
