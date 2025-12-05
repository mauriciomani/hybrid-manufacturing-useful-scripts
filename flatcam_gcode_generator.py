G28 X Y
G0 X44.5 Y81 F3000
G28 Z
G0 Z10 F1000

G29 L34 R55 F65 B97
M420 S1  

G0 Z10 F1000         
G0 X34 Y65 F3000 

0 Z55 F500 ; Raise Z axis 35mm make sure you have enough room
M00 ; Pause and wait for the tool change
G28 Z ; Home the Z axis to establish the new Z position
G00 Z5.0000 F500 ; Lift off touchplate
M00 ; Pause to remove the touchplate


# Remove G21
# Remove G94
# Remove M5
