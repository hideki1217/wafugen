
# For Frontend Developers

1. Ask to hideki1217 about .env including API Key
2. Run the commands below
    ```
    make run_backend
    ```

# For Backend Developers

1. Ask to hideki1217 about .env including API Key
2. Run the commands below
  ```
  ./local_devenv.sh
  ```

# How to deploy

1. docker login to [azure container registry](acrwafugensensui.azurecr.io)
2. ```make deploy_backend ```

# API endpoint

```
GET/v1/report?videoId={str[]: Youtube公式Video識別子たち}

return {
    items: [
        {
            status: str: Ok or ErrorMessage,
            videoId: str, 
            tsuriScore: int(lower=0, upper=100), 
            tsuriReport: {*}
        }
    ]
}

// ExampleCommand: 
// curl 'http://localhost:40000/v1/report?videoId=hGk_ez5di2g,BEygUktR-Jg'
```

# API endpoint url
```
release: wafugen-hacks-api.azurewebsites.net
debug:   localhost:40000
```

