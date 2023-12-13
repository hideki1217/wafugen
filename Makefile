
run_backend:
	docker build -t backend ./backend
	docker run -it --rm -v ./backend:/workspace -p 40000:40000 backend /bin/bash /workspace/run.sh
