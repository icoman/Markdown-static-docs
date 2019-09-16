# Markdown Static Docs Server

This is an web server application written in [Python](https://www.python.org/) 
which serve static **Markdown** pages.

I created this application to help me generate better documentation 
for my [github](https://github.com/) projects.

The application works on both **Python 2.7** and **Python 3.x**.

The server looks for text files with **md** extension to render as 
**Markdown** document and, if no document found, try to return a static file.

The file **README.md** is the default index file.

Install required packages

```bash
pip install bottle
pip install waitress
pip install markdown
```

and start server using **run-server.cmd** file (from project) or a unix batch file.

Before to start the server, edit the batch file and set 
environment variable **MD_FOLDER** to the folder of **Markdown** (*.md) documents.

