group "default" {
    targets = ["main", "scrape"]
}

target "main" {
    dockerfile = "Dockerfile"
    target = "run"
    tags = ["ghcr.io/codl/pokemonrates/pokemonrates"]
}

target "scrape" {
    inherits = ["main"]
    target = "scrape"
    tags = ["ghcr.io/codl/pokemonrates/scrape"]
}

target "test" {
    inherits = ["main"]
    target = "test"
    tags = ["ghcr.io/codl/pokemonrates/test"]
}
