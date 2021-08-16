# Toptal task


### To start the service

```
docker-compose up --build -d
```
- You can reach the API at `localhost:8000`
- You can find the swagger docs at `localhost:8000/docs`
- You can find the prometheus metrics at `localhost:8000/metrics`


### To run the tests
```
bash run_tests.sh
```

### To test the APIs
- Please check `toptal.postman_collection.json` which contains a postman collection that could be used for testing
