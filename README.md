
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

