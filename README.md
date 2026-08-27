[validate_badge]: https://img.shields.io/github/actions/workflow/status/luis-garza/movistar_rft8115vw/validate.yaml?logo=github
[validate_url]: https://github.com/luis-garza/movistar_rft8115vw/actions/workflows/validate.yaml

[release_badge]: https://img.shields.io/github/release/luis-garza/movistar_rft8115vw.svg?logo=github&color=lightgrey
[release_url]: https://github.com/luis-garza/movistar_rft8115vw/releases/latest

[integration_badge]: https://img.shields.io/badge/dynamic/json?logo=home-assistant&logoColor=white&label=installations&labelColor=41bdf5&color=lightgrey&url=https://analytics.home-assistant.io/custom_integrations.json&query=movistar_rft8115vw.total
[integration_url]: https://my.home-assistant.io/redirect/hacs_repository/?owner=luis-garza&repository=movistar_rft8115vw

[community_badge]: https://img.shields.io/static/v1.svg?logo=home-assistant&logoColor=white&labelColor=41bdf5&label=community&message=forum
[community_url]: https://community.home-assistant.io/t/movistars-askey-rft8115vw/841398

[![GitHub Validate][validate_badge]][validate_url]
[![GitHub Release][release_badge]][release_url]
[![HA integration usage][integration_badge]][integration_url]
[![Community Forum][community_badge]][community_url]

# movistar_rft8115vw

Home Assistant [device tracker](https://www.home-assistant.io/integrations/device_tracker) integration for Movistar's Askey RFT8115VW router.

[![Open HACS repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luis-garza&repository=movistar_rft8115vw&category=integration)

## Details

This integration tracks devices connected to a Movistar's Askey RFT8115VW router.

Every connected device is exposed as a `device_tracker` entity, so it can be assigned to a [person](https://www.home-assistant.io/integrations/person) to enable its presence state.

In order to correctly identify the devices, the host name is used as the device name if available; otherwise the MAC address is used instead.

## Installation

The integration can be deployed using [HACS](<https://hacs.xyz>) or manually. It's highly recommended to use HACS for managing custom integrations, so please consider using it.

### HACS

Open [HACS](<https://hacs.xyz>) in Home Assistant and search for Movistar device tracker integration, or just click next button:

[![Open HACS repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luis-garza&repository=movistar_rft8115vw&category=integration)

### Manual

Download all content from `movistar_rft8115vw` folder, and place it in a new custom component folder as `config/custom_component/movistar_rft8115vw`.

## Set up

To set up the integration, go to **Settings** → **Devices & Services** → **Add Integration** and search for *Movistar Askey RFT8115VW router*. Alternatively, use the following button:

[![Add integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=movistar_rft8115vw)

You will be asked for:

- **Host:** Router's hostname or IP address, usually `192.168.0.1` or `192.168.1.1`.
- **Password:** Router's user login password.

Once the integration is loaded, each connected device is added as a `device_tracker` entity. New devices are picked up automatically on the next scan.

Two options can be adjusted from the integration's options (**Settings** → **Devices & Services** → *Movistar Askey RFT8115VW router* → **Configure**):

- **Scan interval (seconds):** how often to poll the router, default `60`.
- **Consider home (seconds):** how long after a device is last seen before it is marked `not_home`, default `180`.

## Troubleshooting

### Enable debug logs

Enable them from the UI, go to **Settings** → **Devices & Services** → *Movistar Askey RFT8115VW router* → ⋮ → **Enable debug logging**.

### Setup errors

The setup form shows a specific message when something fails:

- **"Unable to reach the router, check the host"** — the router is not reachable. Verify the host/IP, that the router is on, and that Home Assistant is on the same network.
- **"Invalid router password"** — the password is wrong. Use the router's login password.
- **"Unexpected error"** — enable debug logs and report the issue.

### Devices not showing up

- The router is polled every **scan interval** (default `60` seconds); new devices appear on the next scan.
- A device is marked `not_home` after **consider home** (default `180` seconds) since it was last seen. Detection granularity is the scan interval, so keep it smaller than `consider home`.
- Both values are changed in **Settings** → **Devices & Services** → *Movistar Askey RFT8115VW router* → **Configure**.

### Change host or password

The host and password are set when adding the integration and cannot be edited afterwards. To change them, delete the integration and add it again.

## References

The first version of this integration was based on [askey_rft3505](https://github.com/jotacor/homeassistant-custom_components) integration from [Jotacor](https://github.com/jotacor).

## Support me

Did you find this integration useful? Please let me know it.

Still want to thank it? Just invite me a beer!

<a href="https://www.buymeacoffee.com/lgarza"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a beer&emoji=🍺&slug=lgarza&button_colour=FFDD00&font_colour=000000&font_family=Poppins&outline_colour=000000&coffee_colour=ffffff"/>
