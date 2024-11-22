input_player = require("input_player")
local lfs = require("lfs_ffi")
local path = [[Resources\\plugins\\FlyWithLua\\Modules\\input_player]]

coro = false -- corutina actual

-- crear entradas del menu
for file in lfs.dir(path) do
    if string.sub(file, -4) == ".csv" then
        add_macro(file, [[
            coro = coroutine.create(
                function()
                    input_player.play("]] .. file .. [[")
                end
            )]])
    end
end

do_every_draw("loop()")
function loop()
    if coro and coroutine.status(coro) == "suspended" then
        coroutine.resume(coro)
    end
end
