#!/usr/bin/python
"""
Create a json file using http://www.keyboard-layout-editor.com/

Use that file to create a kicad schematic and pcb with the switches.
"""

import six
import json
import codecs
from time import time
from pprint import pprint

import pcbnew
kicad = pcbnew.IO_MGR.PluginFind(pcbnew.IO_MGR.KICAD)

mx_lib = "/Library/Application Support/kicad/modules/Keyboard.pretty"
mx_part = "MXALPS"
diode_lib = "/Library/Application Support/kicad/modules/Diodes_ThroughHole.pretty"
diode_part = "Diode_DO-35_SOD27_Horizontal_RM10"
layout_file_name = "103key-layout.json"
project_name = "103key10x11"
output_directory = project_name + "-project/"

spacing = 19.05 * 10**6  # 19mm
x_origin = 2.0
y_origin = 1.5

sw_spacing = 1000
sw_x_origin = 100
sw_y_origin = 100

led_spacing = 1000
led_x_origin = 100
led_y_origin = 6000

diode_x_offset = -9 * 10**6
diode_y_offset = -5 * 10**6

schem_template_header = """EESchema Schematic File Version 2
LIBS:74xx
LIBS:cherrymx
LIBS:device
LIBS:power
LIBS:teensy_3.1
LIBS:numbpad-cache
EELAYER 25 0
EELAYER END
$Descr A2 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr"""

schem_template_footer = "$EndSCHEMATC"

project_template = """update=Friday, March 25, 2016 'PMt' 09:12:47 PM
version=1
last_client=kicad
[pcbnew]
version=1
LastNetListRead=
UseCmpFile=1
PadDrill=0.600000000000
PadDrillOvalY=0.600000000000
PadSizeH=1.500000000000
PadSizeV=1.500000000000
PcbTextSizeV=1.500000000000
PcbTextSizeH=1.500000000000
PcbTextThickness=0.300000000000
ModuleTextSizeV=1.000000000000
ModuleTextSizeH=1.000000000000
ModuleTextSizeThickness=0.150000000000
SolderMaskClearance=0.000000000000
SolderMaskMinWidth=0.000000000000
DrawSegmentWidth=0.200000000000
BoardOutlineThickness=0.100000000000
ModuleOutlineThickness=0.150000000000
[cvpcb]
version=1
NetIExt=net
[general]
version=1
[eeschema]
version=1
LibDir=
[eeschema/libraries]
LibName1=74xx
LibName2=cherrymx
LibName3=device
LibName4=power
LibName5=teensy_3.1
"""

comp_tempate = u"""$Comp
L MX_LED %(ref)s
U %(pkg)d 1 %(timestamp)x
P %(x)d %(y)d
F 0 "%(ref)s" H %(x)d %(ref_y)d 60  0000 C CNN
F 1 "MX_LED" H %(x)d %(y)d 60  0001 C CNN
F 2 "" H %(x)d %(y)d 60  0000 C CNN
F 3 "xasf" H %(x)d %(y)d 60  0000 C CNN
    %(pkg)d    %(x)d %(y)d
    1    0    0    -1
$EndComp
"""


def place_footprint(pcb, x, y, reference=None, i=None):
    # Place the switch
    fp = kicad.FootprintLoad(mx_lib, mx_part)
    pcb.Add(fp)
    fp.Rotate(pcbnew.wxPoint(0, 0), 1800)
    fp.SetPosition(pcbnew.wxPoint(x * spacing, y * spacing))
    if reference is None:
        reference = "SW%d_%d" % (x, y)
    fp.SetReference(reference)
    fp.SetValue(reference)
    fp.SetLocked(True)
    # Place the diode
    fp = kicad.FootprintLoad(diode_lib, diode_part)
    pcb.Add(fp)
    fp.Rotate(pcbnew.wxPoint(0, 0), 2700)
    fp.SetPosition(pcbnew.wxPoint(x * spacing + diode_x_offset, y * spacing + diode_y_offset))
    if i is not None:
        reference = "D%d" % (i)
    if reference is None:
        reference = "D%d_%d" % (x, y)
    fp.SetReference(reference)
    fp.SetValue(reference)
    fp.SetLocked(True)


def add_to_schematic(schem, x, y, timestamp=None, reference=None):
    if reference is None:
        reference = "sw%d_%d" % (x, y)
    schem.write(comp_tempate % {
        "x": x * sw_spacing + sw_x_origin,
        "y": y * sw_spacing + sw_y_origin,
        "ref_y": y * sw_spacing + sw_y_origin - 150,
        "pkg": 1,
        "ref": unicode(reference),
        "timestamp": time() if timestamp is None else timestamp
    })
    schem.write(comp_tempate % {
        "x": x * led_spacing + led_x_origin,
        "y": y * led_spacing + led_y_origin,
        "ref_y": y * led_spacing + led_y_origin - 150,
        "pkg": 2,
        "ref": unicode(reference),
        "timestamp": time() if timestamp is None else timestamp + 1
    })


def main():
    with open(output_directory + project_name + "_v2.pro", mode="w") as project_file:
        project_file.write(project_template)
    with open(layout_file_name) as lautout_file:
        layout = json.load(lautout_file)
    switch_sch = codecs.open(output_directory + project_name + "_v2.sch", mode="w", encoding='utf-8')
    switch_sch.write(schem_template_header)
    pcb = pcbnew.BOARD()
    x, y = x_origin, y_origin
    i = 1
    timestamp = time()
    for row in layout:
        if not isinstance(row, list):
            continue
        x = x_origin
        y_offset = 0.0
        width = 1.0
        for col in row:
            if isinstance(col, dict):
                y_offset = (float(col.get("h", 1)) - 1) / 2
                width = float(col.get("w", 1))
                x += float(col.get("x", 0))
                y += float(col.get("y", 0))
                print col, x, y, width, y_offset
            elif isinstance(col, six.string_types):
                print col, x, y, width, y_offset
                ref = "SW_X%dY%d" % (x, y)
                if col.split() and col.split()[0].isalnum():
                    ref = u"SW_" + col.split()[0]
                ref += "_%d" % i
                x_offset = (width - 1.0) / 2
                place_footprint(pcb, x + x_offset, y + y_offset, ref, i)
                add_to_schematic(switch_sch, x + x_offset, y + y_offset, timestamp + i, ref)
                x += width
                width = 1.0
                i += 1
        y += 1
    pcb.Save(output_directory + project_name + "_v2.kicad_pcb")
    switch_sch.write(schem_template_footer)
    switch_sch.close()

if __name__ == "__main__":
    main()
