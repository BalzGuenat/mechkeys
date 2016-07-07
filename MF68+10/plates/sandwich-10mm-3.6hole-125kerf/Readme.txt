DXF files for a sandwich style case.

switch  - switch plate
closed  - sandwich with no openings
open  - sandwich with opening for cable
bottom-reset  - bottom plate with hole to reach teensy reset
bottom-open  - bottom plate with large opening for teensy and USB cable
Ponoko-P3  - 6 layer sandwich ready for ordering at ponoko.com. Just enough material if ordered in 3mm acrylic.

They were generated with http://builder.swillkb.com/ with following settings:

Switch Type: t:2 (MX+Alps)
Stabilizer Type: s:1 (Cherry+Costar)
Case Type: sandwich
Mount Holes: 8
Hole Diameter: 3.6 (should handle M3.5 and 6-32)
Width Padding: 10mm
Height Padding: 10mm
Plate Corners: 3mm
Kerf: 0.125mm

Layout:

[{a:7},"F1","F2",{x:0.25,a:4},"~\n`","!\n1","@\n2","#\n3","$\n4","%\n5","^\n6","&\n7","*\n8","(\n9",")\n0","_\n-","+\n=",{w:2},"Backspace",{x:0.25,a:7},"Ins","PgUp"],
["F3","F4",{x:0.25,w:1.5},"Tab","Q","W","E","R","T","Y","U","I","O","P","{","}",{w:1.5},"|",{x:0.25},"Del","PgDn"],
["F5","F6",{x:0.25,w:1.75},"Caps Lock","A","S","D","F","G","H","J","K","L",":","\"",{w:2.25},"Enter"],
["F7","F8",{x:0.25,w:2.25},"Shift","Z","X","C","V","B","N","M","<",">","?",{w:2.75},"Shift",{x:0.25},"↑"],
["F9","F10",{x:0.25,w:1.25},"Ctrl",{w:1.25},"Win",{w:1.25},"Alt",{w:6.25},"",{a:4,w:1.25},"Alt",{w:1.25},"Win",{w:1.25},"Menu",{x:0.5,a:7},"←","↓","→"]
