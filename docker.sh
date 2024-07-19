docker pull rabbitmq:management
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
docker build -t final_project .
docker run -it --ipc=host --network host -v {update your absolute path here}/final_project/:/home/final_project --name final_project --privileged final_project
