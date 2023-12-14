
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
GET/v1/report?youtube_ids = {str[]: Youtube公式識別子たち}

return {
    num_items: int,
    reports: [
        youtube_id: str, 
        tsuri_score: int(lower=0, upper=100), 
        tsuri_report: {*}
    ]
}

// ExampleCommand: 
// curl 'http://localhost:40000/v1/report?youtube_ids=\[youtube\]'
```

