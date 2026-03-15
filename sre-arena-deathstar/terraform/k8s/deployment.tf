resource "kubernetes_namespace" "sre" {
  metadata {
    name = "sre"
  }
}

resource "kubernetes_deployment" "sre_backend" {
  metadata {
    name      = "sre-backend-arena"
    namespace = kubernetes_namespace.sre.metadata[0].name
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "sre-backend-arena"
      }
    }

    template {
      metadata {
        labels = {
          app = "sre-backend-arena"
        }
      }

      spec {
        container {
          name  = "app"
          image = "sre-backend-arena:latest"
          port {
            container_port = 8000
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
          }
        }
      }
    }
  }
}
