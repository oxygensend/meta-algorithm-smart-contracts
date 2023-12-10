# meta-algorytm-smart-contracts

Build image

```
docker build . -t meta_environment
```

Run container in terminal mode
```
docker run -it --rm  meta_environment bash 
```

Run container in terminal mode with volumes on app and contracts directories
```
docker run -it --rm -v ./app:/src/app -v ./contracts:/src/contracts meta_environment bash 
```

