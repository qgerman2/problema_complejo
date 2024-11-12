local csv = require("lib.csv")
local f = csv.open("datos.csv")
for fields in f:lines() do
    local t = fields[1] -- segundos
    local aileron = fields[3]
    local elevator = fields[4]
    local throttle = fields[5]
    local rudder = fields[6]
    print(t, aileron, elevator, throttle, rudder)
end