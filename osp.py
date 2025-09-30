# profile.py: A geni-lib script to deploy ubuntu24.04

"""
Simple deployment of Ubuntu 24.04.

Instructions:
## Basic Instructions

Wait for the pc node's `Status` to change to `ready`.
"""

#!/usr/bin/env python

# Import the necessary geni-lib libraries.
# geni.portal is used for defining user-configurable parameters.
# geni.rspec.pg is for defining the resources in the ProtoGENI RSpec format.
import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab
import geni.rspec.igext as ig
import geni.rspec as rspec

# Create a portal context object.
# This is the main interface to the CloudLab portal environment.
pc = portal.Context()

# === Profile Parameters ===
# Define user-configurable parameters that will appear
# on the CloudLab instantiation page.

# Parameter for selecting the OS image.
# Note: You can find other images and their URNs at:
# https://www.cloudlab.us/images.php
pc.defineParameter(
    "osImage", "Operating System Image",
    portal.ParameterType.IMAGE,
    "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU24-64-STD",
    longDescription="OS image for all nodes. Ubuntu 24.04 is used here."
)


# Parameter for selecting the physical hardware type.
# An empty string lets CloudLab choose the best available type.
# Specifying a type (e.g., 'd8545', 'nvidiagh') ensures hardware homogeneity.[11]
pc.defineParameter(
    "hwType", "Hardware Type",
    portal.ParameterType.NODETYPE,
    "d760-hgpu", # Default to nvidiagh nodes.
    longDescription="Specify a hardware type for all nodes. Clear Selection for any available type. d760-hgpu, d8545, nvidiagh, "
)

# Retrieve the bound parameters from the portal context.
params = pc.bindParameters()

# === Resource Specification ===
# Create a request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Create a LAN object to connect all nodes.
lan = request.LAN("lan")


comp = request.RawPC("node")
comp.disk_image = params.osImage
if params.hwType:
    comp.hardware_type = params.hwType

# Add the controller node to the LAN.
iface_pc = comp.addInterface("if0")
lan.addInterface(iface_pc)
iface_pc.component_id = "eth0"


# === Finalization ===
# Print the generated RSpec to the CloudLab portal, which will then use it
# to provision the experiment.
pc.printRequestRSpec(request)
