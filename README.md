## A distant scanner based on Raspberry Pi

The idea is to have a small raspberry at the office that you can send mail to.
When you send him a mail whose object is scan this and with an image attachement, it will resize and clean the image so it looks like a real scanned image and send it back to you as a reply.

```
python scan.py --image nameOfImage.jpg
```

will produce a file `out.pdf` with the processed image.


This script for cleaning is inspired by pyimageseach.


## Logins

In a `login.json` at the root of the project:

```
{"host": "gmail.com", "password": "yourpassword", "message": "test", "user": "bxnode.scan@gmail.com", "port": 587}
```


## Dependency

You'll need opencv installed:

```
sudo apt-get -y install libopencv-dev python-opencv
```
