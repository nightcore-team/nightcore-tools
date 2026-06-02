variable "image_tag" {
  type    = string
  default = "latest"
}

variable "repository" {
  type    = string
}


job "nightcore-tools-bot" {
  datacenters = ["dc1"]
  type        = "service"

  update {
    max_parallel     = 0
    min_healthy_time = "15s"
    auto_revert      = false
  }

  group "nightcore-tools-bot" {
    count = 1

    disconnect {
      lost_after = "40s"
    }

    task "nightcore-tools-bot" {
      driver = "docker"

      vault {
        role = "runner-nightcore-tools"
      }

      identity {
        name = "vault_default"
        aud  = ["vault.io"]
        ttl  = "1h"
      }

      template {
        data = <<EOT
{{ with secret "secret/data/ci/github-registry" }}
REGISTRY_USERNAME={{ .Data.data.username }}
REGISTRY_TOKEN={{ .Data.data.token }}
{{ end }}
EOT
        destination = "secrets/registry.env"
        env         = true
        change_mode = "restart"
      }

      resources {
        cpu    = 150
        memory = 200
      }

      config {
        image = "ghcr.io/${var.repository}:${var.image_tag}"

        network_mode = "host"

        auth {
          username       = "${REGISTRY_USERNAME}"
          password       = "${REGISTRY_TOKEN}"
        }
      }

      template {
        data = <<EOT
{{ with secret "secret/data/ci/repos/nightcore-tools" }}
BOT_TOKEN={{ .Data.data.BOT_TOKEN }}
{{ end }}
EOT
        destination = "secrets/bot.env"
        env         = true
      }

      logs {
        max_files     = 3
        max_file_size = 10
      }

    }
  }
}