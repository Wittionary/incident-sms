if [[ $(git pull git@github.com:wittionary/incident-sms) != "Already up to date." ]]; then
        cd ~/incident-sms
        git pull git@github.com:wittionary/incident-sms
        TAG=`date "+%Y%m%d%H%M"`
        docker build -t incident-sms:$TAG .
        docker stop incident-sms
        docker rm incident-sms
        docker run -d -p 5000:5000 --name incident-sms --restart unless-stopped incident-sms:$TAG
else
        echo "up to date"
fi