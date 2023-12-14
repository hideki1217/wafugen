
# For Frontend Developers

- How to run this server in your local machine
    ```
    make run_backend
    ```

# For Backend Developers

- How to create dev environment
  ```
  ./local_devenv.sh
  ```

# API endpoint

```
GET/v1/report?video_id={str[]: Youtube公式Video識別子たち}

return {
    items: [
        {
            video_id: str, 
            tsuri_score: int(lower=0, upper=100), 
            tsuri_report: {*}
        }
    ]
}

// ExampleCommand: 
// curl 'http://localhost:40000/v1/report?video_id=hGk_ez5di2g,BEygUktR-Jg'
```

