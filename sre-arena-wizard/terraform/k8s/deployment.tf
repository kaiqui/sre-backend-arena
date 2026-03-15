resource "kubernetes_namespace" "sre" {
  metadata {
    name = "sre"
  }
}

resource "kubernetes_deployment" "wizard_api" {
  metadata {
    name      = "wizard-api"
    namespace = kubernetes_namespace.sre.metadata[0].name
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "wizard-api"
      }
    }

    template {
      metadata {
        labels = {
          app = "wizard-api"
        }
      }

      spec {
        container {
          name  = "wizard-api"
          image = "wizard-api:latest"
          port {
            container_port = 8080
          }

          resources {
            requests = {
              cpu    = "200m"
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
