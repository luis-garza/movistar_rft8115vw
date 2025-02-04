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

Any device connected is recorded in [known_devices.yaml](<https://www.home-assistant.io/integrations/device_tracker/#known_devicesyaml>) file and tracked properly. Once a device is tracked, it can be assigned to a [person](https://www.home-assistant.io/integrations/person) to enable its presence state.

In order to correctly identify the devices, the host name is used as device name if it's available, if it isn't then the MAC address is used instead.

## Installation

The integration can be deployed using [HACS](<https://hacs.xyz>) or manually. It's highly recommended to use HACS for managing custom integrations, so please consider using it.

### HACS

Open [HACS](<https://hacs.xyz>) in Home Assistant and search for Movistar device tracker integration, or just click next button:

[![Open HACS repository](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=luis-garza&repository=movistar_rft8115vw&category=integration)

### Manual

Download all content from `movistar_rft8115vw` folder, and place it in a new custom component folder as `config/custom_component/movistar_rft8115vw`.

## Set up

To set up the integration, place the following snippet in [configuration.yaml](<https://www.home-assistant.io/docs/configuration>) file.

```yaml
# Movistar Askey RFT8115VW
device_tracker:
  - platform: movistar_rft8115vw
    host: <router address>
    password: <router password>
    interval_seconds: 60
    consider_home: 360
    new_device_defaults:
      track_new_devices: false
```

Change the following parameters accordingly:

- **host:** Router's hostname or IP address, usually 192.168.1.1 or 192.168.0.1.
- **password:** Router's user login password.
- **interval_seconds:** Seconds between each scan for new devices, default `12`.
- **consider_home:** Seconds to consider a device as `not home` after not being seen, default `180`.
- **track_new_devices:** Track by default every discovered device, either way
will be recorded in [known_devices.yaml](<https://www.home-assistant.io/integrations/device_tracker/#known_devicesyaml>) file.

For more information about the [device tracker](https://www.home-assistant.io/integrations/device_tracker) parameters check the official Home Assistant Documentation.

Finally, restart Home Assistant to load and start the integration.

## Troubleshooting

To enable debug logs just place next snippet in [configuration.yaml](<https://www.home-assistant.io/docs/configuration>) file.

```yaml
logger:
  default: warn
  logs:
    custom_components.movistar_rft8115vw: debug
```

## References

This integration is based on [askey_rft3505](https://github.com/jotacor/homeassistant-custom_components) integration from [Jotacor](https://github.com/jotacor).

## Support me

Did you find this integration useful? Please let me know it.

Still want to thank it? Just invite me a beer!

<a href="https://www.buymeacoffee.com/lgarza"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a beer&emoji=🍺&slug=lgarza&button_colour=FFDD00&font_colour=000000&font_family=Poppins&outline_colour=000000&coffee_colour=ffffff"/>
