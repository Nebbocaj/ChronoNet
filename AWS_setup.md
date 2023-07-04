https://medium.com/saarthi-ai/ec2apachedjango-838e3f6014ab

apache config:

```
<VirtualHost *:80>
ServerAdmin webmaster@example.com
DocumentRoot /home/ubuntu/django/senior-design/ChronoNet
ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined

Alias /static /home/ubuntu/django/senior-design/ChronoNet/static
<Directory /home/ubuntu/django/senior-design/ChronoNet/static>
  Require all granted
</Directory>

Alias /media /home/ubuntu/django/senior-design/ChronoNet/media/
<Directory /home/ubuntu/django/senior-design/ChronoNet/media/>
  Require all granted
</Directory>

<Directory /home/ubuntu/django/senior-design/ChronoNet/config>
	<Files wsgi.py>
	  Require all granted
	</Files>
</Directory>

WSGIDaemonProcess ChronoNet python-path=/home/ubuntu/django/senior-design/ChronoNet python-home=/home/ubuntu/django/chronoenv
WSGIProcessGroup ChronoNet
WSGIScriptAlias / /home/ubuntu/django/senior-design/ChronoNet/config/wsgi.py

</VirtualHost>
```
