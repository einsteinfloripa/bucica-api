.PHONY:	all build-dev-images

all:	build-image

dev: ## Start Application in Development mode
	@poetry run uvicorn src.main:app --reload

deploy-staging: ## Deploy to Staging
	@docker compose -f docker/staging/docker-compose.yml --env-file .env.staging build --no-cache --pull
	@docker compose -f docker/staging/docker-compose.yml --env-file .env.staging up -d
	@docker image prune -f

deploy-production: ## Deploy to Production
	@docker compose -f docker/production/docker-compose.yml --env-file .env.production build --no-cache --pull
	@docker compose -f docker/production/docker-compose.yml --env-file .env.production up -d
	@docker image prune -f

deploy-nginx: ## Deploy Nginx
	@docker compose -f docker/nginx/docker-compose.yml build --no-cache --pull
	@docker compose -f docker/nginx/docker-compose.yml up -d
	@docker image prune -f

help: ## Show this help.
# `help' function obtained from GitHub gist: https://gist.github.com/prwhite/8168133?permalink_comment_id=4160123#gistcomment-4160123
	@echo Shortly API
	@awk 'BEGIN {FS = ": .*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+(\\:[$$()% 0-9a-zA-Z_-]+)*:.*?##/ { gsub(/\\:/,":", $$1); printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL=help
