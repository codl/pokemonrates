group "default" {
    targets = ["main", "scrape"]
}

target "main" {
    dockerfile = "Dockerfile"
    tags = ["ghcr.io/codl/pokemonrates/pokemonrates"]
}

target "scrape" {
    inherits = ["main"]
    target = "scrape"
    tags = ["ghcr.io/codl/pokemonrates/scrape"]
}

target "scrape" {
    inherits = ["main"]
    target = "test"
    tags = ["ghcr.io/codl/pokemonrates/test"]
}
