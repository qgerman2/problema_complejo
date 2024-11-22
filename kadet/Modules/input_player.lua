local csv = require("csv")
local path = [[Resources\\plugins\\FlyWithLua\\Modules\\input_player\\]]

local function play(filename)
    local filepath = path .. filename
    print(filepath)
    local f, err = csv.open(filepath)
    if f == nil then
        print("Error: " .. err)
        return
    end

    -- datarefs de entrada
    set("sim/operation/override/override_joystick", 1)
    set("sim/operation/override/override_joystick_roll", 1);
    set("sim/operation/override/override_joystick_pitch", 1);
    set("sim/operation/override/override_joystick_heading", 1);
    set("sim/operation/override/override_throttles", 1);

    local t0_sim = 0
    local t0_csv = 0
    local pcsv = {}

    local i = 0;
    -- iterar sobre filas del csv
    for fields in f:lines() do
        if i > 0 then
            -- tiempos
            if i == 1 then
                t0_sim = get("sim/time/local_time_sec")
                t0_csv = fields[1]
            end

            -- variables actuales
            local csv = {
                fields[3],
                fields[4],
                fields[5],
                fields[6],
                t = fields[1] - t0_csv
            }

            -- iteracion con acceso a valores actuales y previos
            if i > 1 then
                while true do
                    local t = get("sim/time/local_time_sec") - t0_sim

                    -- ver si toca acceder a siguiente fila
                    if t > csv.t then
                        break
                    end

                    -- interpolar entre pcsv y csv
                    local s = (t - pcsv.t) / (csv.t - pcsv.t)
                    local out = {}
                    for i, v in ipairs(csv) do
                        -- interpolar linealmente ancho de pulso entre t-1 y t
                        local pwm = s * (csv[i] - pcsv[i]) + pcsv[i]
                        -- normalizar
                        out[i] = map_range(1000, 2000, -1, 1, pwm)
                    end

                    -- escribir controles
                    set("sim/joystick/yoke_roll_ratio", out[1])
                    set("sim/joystick/yoke_pitch_ratio", out[2])
                    set_array("sim/flightmodel/engine/ENGN_thro_use", 0, map_range(-1, 1, 0, 1, out[3]))
                    set("sim/joystick/yoke_heading_ratio", out[4])

                    -- mostrar en pantalla
                    -- marco
                    graphics.set_color(0, 0, 0, 0.2)
                    graphics.draw_rectangle(SCREEN_WIDTH - 280, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 10,
                        SCREEN_HEIGHT - 60)
                    -- circulos
                    graphics.set_color(1, 1, 1, 0.1)
                    graphics.set_width(20)
                    graphics.draw_circle(SCREEN_WIDTH - 210, SCREEN_HEIGHT - 130, 60, 1)
                    graphics.draw_circle(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 130, 60, 1)
                    graphics.draw_line(SCREEN_WIDTH - 210, SCREEN_HEIGHT - 130 - 60, SCREEN_WIDTH - 210,
                        SCREEN_HEIGHT - 130 + 60)
                    graphics.draw_line(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 130 - 60, SCREEN_WIDTH - 80,
                        SCREEN_HEIGHT - 130 + 60)
                    graphics.draw_line(SCREEN_WIDTH - 210 - 60, SCREEN_HEIGHT - 130, SCREEN_WIDTH - 210 + 60,
                        SCREEN_HEIGHT - 130)
                    graphics.draw_line(SCREEN_WIDTH - 80 - 60, SCREEN_HEIGHT - 130, SCREEN_WIDTH - 80 + 60,
                        SCREEN_HEIGHT - 130)
                    -- entrada
                    graphics.set_color(1, 1, 1, 1)
                    graphics.draw_filled_circle(SCREEN_WIDTH - 210 + out[1] * 60, SCREEN_HEIGHT - 130 + out[2] * 60, 3)
                    graphics.draw_filled_circle(SCREEN_WIDTH - 80 + out[4] * 60, SCREEN_HEIGHT - 130 + out[3] * 60, 3)

                    coroutine.yield()
                end
            end

            -- valores previos
            pcsv = csv
        end
        i = i + 1
    end

    -- datarefs de salida
    set("sim/operation/override/override_joystick", 0)
    set("sim/operation/override/override_joystick_roll", 0);
    set("sim/operation/override/override_joystick_pitch", 0);
    set("sim/operation/override/override_joystick_heading", 0);
    set("sim/operation/override/override_throttles", 0);
end

-- https://rosettacode.org/wiki/Map_range#Lua
function map_range(a1, a2, b1, b2, s)
    return b1 + (s - a1) * (b2 - b1) / (a2 - a1)
end

return { play = play }
