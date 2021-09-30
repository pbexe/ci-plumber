# Azure


## Subcommands

```console
Usage: ci-plumber azure [OPTIONS] COMMAND [ARGS]...

  Tools to manage deploying to Azure

Options:
  --help  Show this message and exit.

Commands:
  create-db                 Create a database in Azure
  create-registry           Create a new Azure Container Registry
  deploy                    Creates an azure web app
  list-subscriptions        List Azure subscriptions.
  login                     Log in to Azure using Azure CLI.
  set-default-subscription  Set default subscription.
```

### Creating a Database

```console
Usage: ci-plumber azure create-db [OPTIONS]

  Create a database in Azure

Options:
  --name TEXT                     Enter a unique name that identifies your
                                  Azure Database for MariaDB server. The
                                  server name can contain only lowercase
                                  letters, numbers, and the hyphen (-)
                                  character. It must contain between 3 and 63
                                  characters.  [default: my-
                                  database-238878051]

  --resource-group TEXT           The name of the resource group to use.
                                  [default: myResourceGroup]

  --sku [B_Gen5_1|GP_Gen5_32|MO_Gen5_2]
                                  Database SKU  [default: B_Gen5_1]
  --backup-retention INTEGER      Database backup retention in days.
                                  [default: 7]

  --geo-redundant [Disabled|Enabled]
                                  Whether geo-redundant backups should be
                                  enabled for this server.  [default:
                                  Disabled]

  --location [eastus|eastus2|southcentralus|westus2|westus3|australiaeast|southeastasia|northeurope|swedencentral|uksouth|westeurope|centralus|northcentralus|westus|southafricanorth|centralindia|eastasia|japaneast|jioindiawest|koreacentral|canadacentral|francecentral|germanywestcentral|norwayeast|switzerlandnorth|uaenorth|brazilsouth|centralusstage|eastusstage|eastus2stage|northcentralusstage|southcentralusstage|westusstage|westus2stage|asia|asiapacific|australia|brazil|canada|europe|india|japan|uk|unitedstates|eastasiastage|southeastasiastage|centraluseuap|eastus2euap|westcentralus|southafricawest|australiacentral|australiacentral2|australiasoutheast|japanwest|jioindiacentral|koreasouth|southindia|westindia|canadaeast|francesouth|germanynorth|norwaywest|swedensouth|switzerlandwest|ukwest|uaecentral|brazilsoutheast|qatarcentral]
                                  The Azure location for the server.
                                  [default: uksouth]

  --ssl [Disabled|Enabled]        Whether SSL should be enabled for this
                                  server.  [default: Enabled]

  --storage INTEGER               The storage capacity of the server (the unit
                                  is megabytes). Valid storage sizes are 5,120
                                  MB (minimum) with increases in 1,024-MB
                                  increments.  [default: 51200]

  --version TEXT                  The version of MariaDB to use.  [default:
                                  10.2]

  --admin-username TEXT           The user name for the administrator login.
                                  The admin-user parameter can't be
                                  azure_superuser, admin, administrator, root,
                                  guest, or public.  [default: myadmin]

  --admin-password TEXT           The password of the administrator user. Your
                                  password must contain between 8 and 128
                                  characters. It must contain characters from
                                  three of the following categories: English
                                  uppercase letters, English lowercase
                                  letters, numbers, and non-alphanumeric
                                  characters.  [required]

  --help
```

### Creating a Registry

```console
Usage: ci-plumber azure create-registry [OPTIONS]

  Create a new Azure Container Registry

Options:
  --registry-name TEXT            The name of the registry  [default:
                                  registry-195968669]

  --resource-group-name TEXT      The name of the resource group to use.
                                  [default: myResourceGroup]

  --location [eastus|eastus2|southcentralus|westus2|westus3|australiaeast|southeastasia|northeurope|swedencentral|uksouth|westeurope|centralus|northcentralus|westus|southafricanorth|centralindia|eastasia|japaneast|jioindiawest|koreacentral|canadacentral|francecentral|germanywestcentral|norwayeast|switzerlandnorth|uaenorth|brazilsouth|centralusstage|eastusstage|eastus2stage|northcentralusstage|southcentralusstage|westusstage|westus2stage|asia|asiapacific|australia|brazil|canada|europe|india|japan|uk|unitedstates|eastasiastage|southeastasiastage|centraluseuap|eastus2euap|westcentralus|southafricawest|australiacentral|australiacentral2|australiasoutheast|japanwest|jioindiacentral|koreasouth|southindia|westindia|canadaeast|francesouth|germanynorth|norwaywest|swedensouth|switzerlandwest|ukwest|uaecentral|brazilsoutheast|qatarcentral]
                                  The name of the location to create the
                                  registry in.  [default: uksouth]

  --sku [Basic|Standard|Premium]  The SKU of the registry.  [default: Basic]
  -v, --verbose                   Verbose output.  [default: False]
  --help                          Show this message and exit.
```

### Deploying a Web App

```console
Usage: ci-plumber azure deploy [OPTIONS]

  Creates an azure web app

Options:
  --service-plan TEXT    Service plan name  [default: myServicePlan]
  --app-name TEXT        Application name  [default: myApp-105028613]
  --resource-group TEXT  The name of the resource group to use.  [default:
                         myResourceGroup]

  --os-type TEXT         OS type  [default: linux]
  --image TEXT           The name of the image to use.  [required]
  --login-server TEXT    The name of the login server to use.  [required]
  --registry-name TEXT   The name of the registry to use.  [required]
  -v, --verbose          Verbose output.  [default: False]
  --help                 Show this message and exit.
```

### Listing Subscriptions

```console
Usage: ci-plumber azure list-subscriptions [OPTIONS]

  List Azure subscriptions.

Options:
  --help  Show this message and exit.
  ```

### Changing Active Subscription

```console
Usage: ci-plumber azure set-default-subscription [OPTIONS]

  Set default subscription.

Options:
  --subscription-id TEXT  The subscription ID to set as default.  [required]
  --help                  Show this message and exit.
```

### Logging in to Azure

```console
Usage: ci-plumber azure login [OPTIONS]

  Log in to Azure using Azure CLI.

Options:
  --help  Show this message and exit.
```
