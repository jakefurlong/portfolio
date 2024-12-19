resource "google_compute_instance" "vm_instance" {
  name         = "kubernetes-playground"
  machine_type = "e2-medium"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"

    access_config {
      # Ephemeral IP
    }
  }
}
