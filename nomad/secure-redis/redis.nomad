job "redis" {
  datacenters = ["dc1"]
  type = "service"

  group "redis-server" {
    ephemeral_disk {
      sticky = true
      migrate = true
      size = 300
    }

    task "redis-stunnel-server" {
      driver = "docker"
      config = {
        port_map = {
          stunnel = 46379
        }
        image = "https403/stunnel:latest"  # the only image that does not define an entrypoint
        command = "${NOMAD_TASK_DIR}/stunnel.conf" 
      }
      template {
        data = "redis:44f26f6d54d54d31a8e3548b00be793b"
        destination = "${NOMAD_SECRETS_DIR}/stunnel-psk.txt" 
        perms = "600"
      }

      service {
        name = "redis"
      }

      template {
        destination = "${NOMAD_TASK_DIR}/stunnel.conf"
        data = <<EOH
foreground = yes
pid = {{ env "NOMAD_TASK_DIR" }}/stunnel.pid 

[PSK server]
accept = 46379
connect = {{ env "NOMAD_ALLOC_DIR" }}/redis.sock
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

    task "redis" {
      driver = "docker"
      config {
        image = "redis:3.2"
        args = [
          "--unixsocket ${NOMAD_ALLOC_DIR}/redis.sock",
          "--unixsocketperm 777",
          "--port 0"
        ]
      }
      resources {
        cpu    = 20 # 500 MHz
        memory = 256 # 256MB
        network {
          mbits = 1
        }
      }
    }
  }
}
