# Tell Terraform we are using Azure
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "c3b409f1-53c9-4984-a0ab-56da33521d03"
}

# A resource group: the "folder" for the whole project
resource "azurerm_resource_group" "main" {
  name     = "rg-jobtohired"
  location = "northeurope"
}

# A storage account with Data Lake features turned on
resource "azurerm_storage_account" "lake" {
  name                            = "jobtohiredlake26"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  is_hns_enabled                  = true
  allow_nested_items_to_be_public = false
}

# The three pipeline layers
resource "azurerm_storage_container" "bronze" {
  name                  = "bronze"
  storage_account_id    = azurerm_storage_account.lake.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "silver" {
  name                  = "silver"
  storage_account_id    = azurerm_storage_account.lake.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "gold" {
  name                  = "gold"
  storage_account_id    = azurerm_storage_account.lake.id
  container_access_type = "private"
}

# Who am I? (reads your Azure login details)
data "azurerm_client_config" "current" {}

# The safe for secrets
resource "azurerm_key_vault" "kv" {
  name                       = "kv-jobtohired26"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  rbac_authorization_enabled = true
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
}

# Give YOU permission to add and read secrets in the vault
resource "azurerm_role_assignment" "kv_me" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

# Let ME read and write data in the lake (needed to test the script locally)
resource "azurerm_role_assignment" "lake_me" {
  scope                = azurerm_storage_account.lake.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}