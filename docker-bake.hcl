group "default" {
    targets = ["main", "scrape"]
}

target "main" {
    dockerfile = "Dockerfile"
    tags = ["pokemonrates"]
}

target "scrape" {
    inherits = ["main"]
    target = "scrape"
    tags = ["pokemonrates:scrape"]
}
