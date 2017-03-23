job "app" {
  datacenters = ["dc1"]
  type = "service"


  group "app" {

    task "app" {
      driver = "docker"
      config {
        image = "redis:3.2"
        command = "redis-cli"
        args = [
          "-s", "${NOMAD_ALLOC_DIR}/redis.sock", "INCR", "testkey"
        ]
      }
      resources {
        cpu    = 20
        memory = 32 # 256MB
      }
    }

    task "redis-stunnel-client" {
      driver = "docker"
      config = {
        image = "https403/stunnel:latest"  # the only image that does not define an entrypoint
        command = "${NOMAD_TASK_DIR}/stunnel.conf" 
      }
      template {
        data = "redis:44f26f6d54d54d31a8e3548b00be793b"
        destination = "${NOMAD_SECRETS_DIR}/stunnel-psk.txt" 
        perms = "600"
      }

      template {
        destination = "/local/stunnel.conf"
        data = <<EOH
foreground = yes
pid = {{ env "NOMAD_TASK_DIR" }}/stunnel.pid 

[PSK client]
client = yes
accept = {{ env "NOMAD_ALLOC_DIR" }}/redis.sock
connect = {{ with service "stunnel" }}{{ with index . 0 }}{{ .Address }}:{{ .Port }}{{ end }}{{ end }}
ciphers = PSK
PSKsecrets = {{ env "NOMAD_SECRETS_DIR" }}/stunnel-psk.txt
EOH
      }

      resources {
        cpu    = 20
        memory = 32 # 256MB
        network {
          port "stunnel" {}
          mbits = 1
        }
      }
    }

  }
}
