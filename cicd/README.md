docker run -d --restart=always -p 127.0.0.1:2376:2375 --network cicd_jenkins -v /var/run/docker.sock:/var/run/docker.sock alpine/socat tcp-listen:2375,fork,reuseaddr unix-connect:/var/run/docker.sock

sonar token : squ_c98bd86938107f648ed26248405a533eed183ce8

JenkinsPassword1!