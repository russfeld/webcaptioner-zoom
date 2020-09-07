# Update September 7, 2020

It looks like this feature is now integrated directly into WebCaptioner! So, most likley this repository will be abandoned as it has served its purpose.

https://webcaptioner.com/blog/2020/09/september-2020-updates/

Go buy that developer a coffee instead!

# webcaptioner-zoom

Stream caption requests from Web Captioner to Zoom Meeting by combining [jlacson/webcaptioner-stream](https://github.com/jlacson/webcaptioner-stream) and [Zoom API](https://support.zoom.us/hc/en-us/articles/115002212983-Integrating-a-third-party-closed-captioning-service).
A really rough POC!

## Configuration

Edit `stream.py`, change the variables `ZOOM_API_TOKEN` (`https://wmcc.zoom.us/closedcaption?id={LONG_STRING}`) and `LANGAUGE`.

## Environment Set Up

To get started, set up a virtual environment with Python:

    pip install virtualenv [--user (optional)]

    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Once you are in the virtual environment (shell should be prefaced with `(.venv)`)
run `python3 stream.py` to start a Flask server.

## Generating Keypairs

Web Captioner forces HTTPS by default, so Chrome will by default block
all requests to a standard Flask server because it's not running HTTPS!
No worries, as with a certificate and key we can stand up an HTTPS server.

To generate a private key and certificate, use the following command
and follow the prompts:

    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

In Chrome, to get insecure requests to localhost working, go to the following URL:

    chrome://flags/#allow-insecure-localhost

Set it to enabled and restart the browser.

## Web Captioner Setup

Before starting a transcription, you will need to go to `https://localhost:9999/`
and make sure you see the "Hello World!" page. If you can see that, you've properly
told Chrome to allow insecure requests to content on `localhost`.

After that, go to `https://webcaptioner.com/captioner/settings/webhooks` 
and for the URL enter `https://localhost:9999/transcribe` (Method: `POST`)

## Demo

![Zoom CC Demo](./zoom_cc_demo.gif)
