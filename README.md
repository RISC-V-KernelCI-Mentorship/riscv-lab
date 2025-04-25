# RISC-V Lab

This project includes a containarized solution for polling builds from KernelCI.
After getting the builds the software calls a series of tests runners, which can later submit results to [KCIDB](https://github.com/kernelci/kcidb) using [submit_results.py](riscvlab/submit_results.py).

We make available a [docker-compose.yml](docker-compose.yml) file to make running the project simpler. This file depends on two environment variables:

1. `SECRETS_LOC`: Defines the location of a json file containing all secrets used by the runners.
2. `GITHUB_APP_CERT`: Location of the private key of the GitHub App used to run runners on this repo.

You coul run the project using the following command:

```shell
SECRETS_LOC=secrets.json GITHUB_APP_CERT=github.pem docker compose up
```

## Deployment

The project is currently deployed in an Ubuntu VM as a service we named `poll-builds`.

An example configuration is as follows:

```shell
[Unit]
Description=Poll builds from KernelCI container
After=docker.service
Requires=docker.service

[Service]
Restart=always
Environment="SECRETS_LOC=/home/user/secrets.json"
Environment="GITHUB_APP_CERT=/home/user/github.private-key.pem"
ExecStart=/usr/bin/docker compose -f /home/ubuntu/riscv-lab/docker-compose.yml up
ExecStop=/usr/bin/docker compose -f /home/ubuntu/riscv-lab/docker-compose.yml stop

[Install]
WantedBy=default.target
```

The service can be enabled using:

```shell
systemctl enable poll-builds.service
```

The service can be started using:

```shell
service poll-builds start
```

Restarted with:

```shell
service poll-builds restart
```

And stopped with:

```shell
service poll-builds stop
```

## Runners

The different test runners called after getting the builds can be found in the [runners.yml file](riscvlab/runners/runners.yml).

There are 2 kinds of runners:

1. GitHub Actions:

```shell
  - type: github
    owner: <Org/user who owns the repo> 
    repo: <name of the repo>
    workflow-id: <workflow id or filename>
    secrets-key: <key inside secrets json>
    client-id-key: <key inside secrets json>

```

`secrets-key` is the key inside the secrets json indicating the location of the GitHub App private key. If you're using the `docker-compose.yml` provided in the repo the value in the json will be `/github_cert.pem`.

`client-id-key` is the key inside the secrets json corresponding to the GitHub App client id.

With all of the above, the secrets json file could look like this:

```shell
{
        "private_key_pem": "/github_cert.pem",
        "client_id": "Ibg6rgvjjgsayt8"
}
```

2. RISC-V API:

```shell
  - type: riscv-api
    url: http://localhost/api/v1/riscv-lab/run-tests
    test-collection: kunit
    tests:
      - kunit
```

### GitHub App

The GitHub runners depend on worfklows that can be called via the GitHub REST API (e.g., [kselftest.yml](.github/workflows/kselftest.yml)).

To configure the GitHub app you must follow the steps described in the [GitHub Docs](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow). In our case we configured the app at the organization level.
