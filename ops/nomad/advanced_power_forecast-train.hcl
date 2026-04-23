job "ml-erg-advanced_power_forecast-train" {
 
  type = "batch"
 
  periodic {
    crons            = ["0 4 * * *"]  # e.g., "0 4 * * *" for daily at 4am
    prohibit_overlap = true
    time_zone        = "UTC"
    enabled          = true
  }
 
  group "train" {
    task "train" {
      driver = "docker"
 
      config {
 
        image = "ghcr.io/enlitia/service-core-ml:latest"
        force_pull = true
 
        auth {
            username = "__token__"
            password = "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"
        }

        volumes = [
          "/opt/mlflow-data/mlruns:/app/mlruns"
        ]

        command = "python"
        args = [
          "src/ml/tasks/advanced_power_forecast/train.py",
          "--task-name=advanced_power_forecast"
        ]
      }
 
      env {
        CLIENT_NAME = "erg"
        DB_USER = "app_hub"
        DB_PASSWORD = "2PWcx7VbxCHtRJNwQe1IUovN"
        SM_SETTINGS_MODULE = "production"
      }
 
      resources {
        memory = 1024
      }
    }
  }
}
