resource "kubernetes_namespace" "sre" {
  metadata {
    name = "sre"
  }
}

resource "kubernetes_deployment" "pokemon_battle_api" {
  metadata {
    name      = "pokemon-battle-api"
    namespace = kubernetes_namespace.sre.metadata[0].name
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "pokemon-battle-api"
      }
    }

    template {
      metadata {
        labels = {
          app = "pokemon-battle-api"
        }
      }

      spec {
        container {
          name  = "pokemon-battle-api"
          image = "pokemon-battle-api:latest"
          port {
            container_port = 3000
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
            limits = {
              cpu    = "500m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}
