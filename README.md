# device-mesh

M2M Gateway


## Stack

Group of devices.

* name
* description


## Location

Location, timestamping.

* lat
* lon
* timestamp

## Device

Device.

* stack
* name
* description
* type
* location


## Node

Part of a device.

* device
* name
* description
* tags
* unit
* min_value
* max_value
* current_value

Point

# Datapoint for a given node.

* node
* timestamp
* value