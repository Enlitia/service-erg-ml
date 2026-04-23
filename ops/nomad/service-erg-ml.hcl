job "advanced-power-forecast" {
 
  type = "batch"
 
  periodic {
    crons            = ["0 4 * * *"]
    prohibit_overlap = true
    time_zone        = "UTC"
    enabled          = true
  }
 
  group "advanced-power-forecast" {
    task "advanced-power-forecast" {
      driver = "docker"
 
      config {
 
        image = "ghcr.io/enlitia/advanced-power-forecast:latest"
        force_pull = true
 
        auth {
            username = "__token__"
            password = "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"
        }

        command = "python"
        args = [
          "src/ml/advanced_power_forecast/main.py"
        ]
      }
 
      env {
        DB_USER="app_hub"
        DB_PASSWORD="2PWcx7VbxCHtRJNwQe1IUovN"
        SM_SETTINGS_MODULE="production"
      }
 
      resources {
        memory = 1024
      }
    }
  }
}