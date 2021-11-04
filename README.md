# XRPL Node Detector

The Node Detector is a command-line UI dashboard for XRPL node and validator operators, to make it easier for them to identify problems with their nodes.

![image](https://user-images.githubusercontent.com/8029314/140369880-900852de-953e-41ab-9c22-ef155b49133e.png)

To start it up, create your own `.env` file based on `.env.example` with the path to your `rippled.cfg` file in the variable `CONFIG_FILE`. 

Then, type: `poetry run python -m dashboard.main`

## Tabs
There are three tabs. You can navigate between the tabs using the arrow keys.

### `peers`
The `peers` tab identifies what peers you're connected to.
![image](https://user-images.githubusercontent.com/8029314/140371656-f478fee4-868f-402e-9762-625ca2b3c562.png)

### `config`
The `config` tab inspects your `rippled.cfg` file and determines if there is any problems with it.
![image](https://user-images.githubusercontent.com/8029314/140372217-be975078-a18b-4372-8c79-f37eda5f7a08.png)

### `unl`
The `unl` tab displays the public keys of the UNLs you're connected to.
![image](https://user-images.githubusercontent.com/8029314/140373387-7be71ccf-7e94-4f0f-b62c-1212fc873300.png)
