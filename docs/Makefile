build:
	mdbook build

bind: ## build in docker
	docker run -ti --rm -v $$(pwd):/mnt -w /mnt/ registry.gitlab.com/markuman/container-images:mdbook mdbook build
