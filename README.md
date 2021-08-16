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


### Future work
- Fetch secrets from a secret store (e.g. vault) to encode/decode tokens, i added them in the repo for demonstration purposes
- Add a working ci file, tried but couldnt run it as apparently there's anotehr ci file plugged in behind the scenes
- Better scalable design of rbac for admin rights, or use an external tool like keycloak
- Test performance of api querying on hundreds of runs to see if pandas scales well
- Discuss updates of speed/distance and weather forecast of a run based on the UI use cases
- More flexible mocking to test more usecases with custom timestamps (for distances and speed)
- More e2e testing scenarios
