kubectl delete -f ./micro3/hyeonseong-disPod.yaml &&
sudo docker build -t hsd -f ./micro3/docker/Dockerfile . &&
sudo docker tag hsd hyeonseong0917/hsd &&
sudo docker push hyeonseong0917/hsd &&
kubectl apply -f ./micro3/hyeonseong-disPod.yaml