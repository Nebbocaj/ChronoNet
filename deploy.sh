ssh -i "aws.pem" ubuntu@ec2-3-209-120-160.compute-1.amazonaws.com /bin/bash << EOF
    source django/chronoenv/bin/activate
    cd django/senior-design
    git pull
    cd ChronoNet/
    pip install -r requirements.txt 
    python manage.py makemigrations
    python manage.py migrate
    printf "yes" | python manage.py collectstatic
    sudo chown www-data:www-data db.sqlite3
    sudo chown www-data:www-data media/
    sudo chown www-data:www-data .
    sudo service apache2 restart
EOF