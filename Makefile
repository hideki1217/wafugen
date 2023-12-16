
run_backend:
	docker build -t backend ./backend
	docker run -it --rm -v ./backend:/workspace -p 40000:80 backend


deploy_backend:
	docker build -t backend_deploy:latest -f ./backend/Dockerfile.deploy  ./backend
	docker tag backend_deploy:latest acrwafugensensui.azurecr.io/backend_deploy:latest
	docker push acrwafugensensui.azurecr.io/backend_deploy:latest