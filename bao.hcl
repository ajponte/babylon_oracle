storage "file" {
  path = "./bao-data"
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = true
}

disable_mlock = true
ui = true

secret "kv-v2" {
    path = "secret"
}
