# profile.py: A geni-lib script to deploy ubuntu24.04

"""Simple deployment of Ubuntu 24.04.
"""

#!/usr/bin/env python

# Import the necessary geni-lib libraries.
# geni.portal is used for defining user-configurable parameters.
# geni.rspec.pg is for defining the resources in the ProtoGENI RSpec format.
import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab
import geni.rspec.igext as ig

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
# Specifying a type (e.g., 'd430', 'm510') ensures hardware homogeneity.[11]
pc.defineParameter(
    "hwType", "Hardware Type",
    portal.ParameterType.NODETYPE,
    "A100", # Default to A100 nodes.
    longDescription="Specify a hardware type for all nodes. Clear Selection for any available type."
)

# Parameters for OpenStack authentication.
# These will be used in the DevStack configuration.
# Default values are provided for convenience but should be changed.
pc.defineParameter(
    "os_username", "Username", 
    portal.ParameterType.STRING, 
    "crookshanks",
    longDescription="Custom username for OpenStack authentication (required). Defaulting to 'crookshanks'."
)

pc.defineParameter(
    "os_password", "Password",
    portal.ParameterType.STRING,
    "chocolateFrog!",
    longDescription="Custom password for OpenStack authentication (required). Defaulting to 'chocolateFrog!'."
)

# Retrieve the bound parameters from the portal context.
params = pc.bindParameters()

# === Resource Specification ===
# Create a request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Create a LAN object to connect all nodes.
lan = request.LAN("lan")

# --- Controller Node Definition ---
# This node will run all OpenStack control plane services and
# orchestrate the deployment.
pc = request.RawPC("pc")
pc.disk_image = params.osImage
if params.hwType:
    pc.hardware_type = params.hwType

# Add the controller node to the LAN.
iface_controller = pc.addInterface("if0")
lan.addInterface(iface_controller)

# === Instructions ===
# The 'instructions' text is displayed on the experiment page after the user
# has created an experiment using the profile. Markdown is supported.

instructions = """
## Basic Instructions

Wait for the pc node's `Status` to change to `ready`.

### Login Credentials
Default: `crookshanks` / `chocolateFrog!`
If you changed the default values and forgot what you set it to, click on the `Bindings` tab on the experiment page to see the custom settings.
"""

# Set the instructions to be displayed on the experiment page.
tour = ig.Tour()
# tour.Description = (ig.Tour.MARKDOWN, description)
tour.Instructions(ig.Tour.MARKDOWN,instructions)
request.addTour(tour)

# === Finalization ===
# Print the generated RSpec to the CloudLab portal, which will then use it
# to provision the experiment.
pc.printRequestRSpec(request)
