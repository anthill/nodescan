## A distant scanner based on Raspberry Pi

The idea is to have a small raspberry at the office that you can send mail to.
When you send him a mail whose object is scan this and with an image attachement, it will resize and clean the image so it looks like a real scanned image and send it back to you as a reply.

```
python scan.py --image nameOfImage.jpg
```

will produce a file `out.pdf` with the processed image.


This script for cleaning is inspired by pyimageseach.


## Install

Use

sudo apt-get update
sudo apt-get -y install git git-flow curl unzip zsh python-pip
git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
cp ~/.zshrc ~/.zshrc.orig
cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
chsh -s /bin/zsh
git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
export EDITOR=vim;


sudo apt-get -y install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas
sudo apt-get -y install libopencv-dev python-opencv

sudo apt-get -y install getmail4 mpack
mkdir -p ~/mail/new
mkdir -p ~/mail/cur
mkdir -p ~/mail/tmp

