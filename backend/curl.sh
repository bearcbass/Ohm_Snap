
# curl -X POST -H "Content-Type: application/json" -d '{"coordinates": {"x": 200, "y": 200}}' http://127.0.0.1:5000/mask

curl -X POST -H "Content-Type: multipart/form-data" -F "image=@mongo.py" -F "data={}" http://127.0.0.1:5000/mask


#-F 'data={"coordinates": {"x": 200, "y": 200}};type=application/json'

