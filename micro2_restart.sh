kubectl delete -f ./micro2/hyeonseong-conPod.yaml &&
sudo docker build -t hsc -f ./micro2/docker/Dockerfile . &&
sudo docker tag hsc hyeonseong0917/hsc &&
sudo docker push hyeonseong0917/hsc &&
kubectl apply -f ./micro2/hyeonseong-conPod.yaml