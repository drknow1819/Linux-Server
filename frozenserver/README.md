
# Project 5: _**Linux Server Configuration**_

The Linux Server Configuration project consists of a web application
***"Frozen Market"***  using the Python framework Flask that provides a list of
items within a variety of categories, with the help of WSGI server
and Apache as well..

## Server Configration Steps
#### **1.** Create an instance of Ubuntu on an AWS "Amazon Lightsail"  
* First, log in to Lightsail. If you don't already have an Amazon Web Services
account, you'll be prompted to create one.
* Once you're logged in, Lightsail will give you a friendly message with
a robot on it, prompting you to create an instance
* Now choose an instance image "Ubuntu". First, choose "OS Only". Second,
choose Ubuntu as the operating system.
* Choose your instance plan as you desire.
* Give your instance "Virtual Machine" a hostname.
* **Public IP: 3.15.10.104**
* Download **ssh key** to connect from local terminal as following:
```ssh ubuntu@3.15.10.104 -i downloadedkey```
* Update all currently installed packages
```    sudo apt-get update```
```sudo apt-get upgrade```

#### **2.** Create `grader` user and give it sudo privileges
* ```sudo adduser grader```
* You can leave all the fields blank for now.
* ```sudo nano /etc/sudoers.d/grader```
* Then paste ```grader ALL=(ALL) NOPASSWD:ALL``` then ```Ctrl```+```x```.
* Another way just ```sudo usermod -aG sudo grader```

#### **3.** Create ssh keys for `grader` and add public key to server
* From your local terminal ```ssh-keygen```
* If you opened your terminal from the desired location you can just put
the name of your file and it will be saved in the same path.
* I named my key **Frozen** so i have public and private keys as follow:
```Frozen```
```Frozen.pub```
* From the same terminal get the public key useing:
```cat Frozen.pub```
* Open another terminal and connect to **ubuntu** user.
* Now adding the key through the following commands:
```sudo mkdir /home/grader/.ssh```
```sudo chown -R grader:grader /home/grader/.ssh```
```sudo nano  /home/grader/.ssh/authorized_keys```
* Copy `Frozen.pub` ssh key and paste it in `authorized_keys` then save
the file.
* Now you can login as `grader`.
```ssh grader@3.15.10.104 -i Frozen```
* Prevent users from logging in with passwords
```sudo nano /etc/ssh/sshd_config```
* Then change ```PasswordAuthentication``` value to ```no```

#### **4.** Configureing firewall
* On terminal:
```sudo ufw allow www```
```sudo ufw allow ssh```
```sudo ufw allow 2200/tcp```
```sudo ufw allow 123/udp```
```sudo ufw enabled```
* Then check firewall status:
```sudo ufw status```
* On AWS under **Networking** tab:
Default values will be:
```SSH     TCP     22``` *"Will be deleted later"*
```HTTP    TCP     80```
* Add 2 custom connection with specific ports as following:
```Custom       UDP     123```
```Custom       TCP     2200```
* Delete the `SSH` connection on AWS and relogin using:
```ssh grader@3.15.10.104 -p 2200 -i frozen```
* Close the port in the terminal
```sudo ufw deny 22```

#### **5.** Install all the software we will need
* Make sure you logged in as `grader` then:
```sudo apt-get install apache2```
```sudo apt-get install python```
```sudo apt-get install python-pip```
```sudo apt-get install python-httplib2```
```sudo apt-get install python-requests```
```sudo apt-get install python-sqlalchemy```
```sudo apt-get install python-flask```
```sudo apt-get install libapache2-mod-wsgi python-dev```
```sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib```
```sudo pip install psycopg2-binary```
```sudo pip install oauth2client```

#### **6.** Configure Postgres:
* After installing Postgresql, login as user postgres.
```     sudo -i -u postgres```
* Create new DB named `frozen`.
```     create database frozen;```
* Make password will be used for database connection.
```ALTER USER postgres with encrypted password 'test';```
* Change configration file from `peer` to `md5`.
```     sudo nano /etc/postgresql/9.5/main/pg_hba.conf```
Instead of ```local all postgres peer```
Change to ```local all postgres md5```

#### **7.** Setup the application
* Transfer the app folder from computer to server.
```     sftp -i frozen -P 2200 grader@3.15.10.104```
* Navigate to you local folder with your app folder using `lcd`,
in my case **frozenserver**.
```cd /home/grader/```
```put -rf  frozenserver```
* Finally type ```exit```
* ssh back as `grader`
```sudo cp frozenserver/* /var/www/frozenserver```
```sudo chown -R www-data:www-data /var/www/frozenserver/```
```sudo chmod -R 774 /var/www/frozenserver/```
* Edit Apache configration file:
```sudo nano /etc/apache2/sites-enabled/000-default.conf```
* Paste this code in the file and save it.
```
<VirtualHost *:80>
                ServerName 3.15.10.104
                ServerAdmin hmsorial@gmail.com
                WSGIScriptAlias / /var/www/frozenserver/frozen.wsgi
                <Directory /var/www/frozenserver/frozenserver/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/frozenserver/frozenserver/static
                <Directory /var/www/frozenserver/frozenserver/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
* The `WSGI` file is a simple python app, so you can make the file before push
them to server as i did. it should look like this code.
```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/frozenserver/frozenserver")

from frozen import app as application
```
* Make sure that the create_engine code has been converted to postgresql:
```engine = create_engine('postgresql+psycopg2://postgres:test@localhost/frozen')```

#### **8.** Inialize the database and run the app.
* On the terminal as `grader`:
```sudo python /var/www/frozenserver/frozenserver/setup.py```
```sudo python /var/www/frozenserver/frozenserver/mylist.py```

* Now access the app through [http://3.15.10.104](http://3.15.10.104)


## Usefull Links

- [Flask: Documentation](http://flask.pocoo.org/docs/1.0/)
- [Flask Tutorial](http://flask.pocoo.org/docs/1.0/tutorial/)
- [Stack Overflow](https://stackoverflow.com/)
- [Stack Exchange](https://stackexchange.com/)
- [Apache](http://httpd.apache.org/)
- [ask Ubuntu](https://askubuntu.com/)
- [Chmod Calculator](https://chmod-calculator.com/)
