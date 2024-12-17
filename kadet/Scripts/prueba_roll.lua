add_macro("prueba_roll", [[
    proceso = coroutine.create(prueba_roll)]])

function prueba_roll()
    local MOTOR1 = 0
    print("prueba_roll")

    -- desactivo autopiloto
    set("sim/cockpit/autopilot/autopilot_mode", 0)
    set("sim/cockpit/autopilot/autopilot_state", 0)

    -- override controles
    set("sim/operation/override/override_joystick", 1)
    set("sim/operation/override/override_joystick_roll", 1);
    set("sim/operation/override/override_joystick_pitch", 1);
    set("sim/operation/override/override_joystick_heading", 1);
    set("sim/operation/override/override_throttles", 1);

    -- desactivar fisicas
    set_array("sim/operation/override/override_planepath", 0, 1)
    sleep(1)

    -- setear motor
    set_array("sim/flightmodel/engine/ENGN_running", 0, 1)
    set_array("sim/flightmodel/engine/ENGN_tacrad", 0, 180)
    set_array("sim/flightmodel/engine/POINT_tacrad", 0, 180)
    set_array("sim/flightmodel/engine/ENGN_N1_", 0, 71)
    set_array("sim/flightmodel/engine/ENGN_N2_", 0, 71)

    -- setear posicion velocidad orientacion
    set("sim/flightmodel/position/local_x", 6387.532886598)
    set("sim/flightmodel/position/local_y", 3000)
    set("sim/flightmodel/position/local_z", -31578.836403774)
    set("sim/flightmodel/position/local_vx", 45.629841)
    set("sim/flightmodel/position/local_vy", 0.380211)
    set("sim/flightmodel/position/local_vz", 8.978944)

    local psi = 100.867050
    set("sim/flightmodel/position/psi", psi)

    local tetha = -3.572355
    set("sim/flightmodel/position/theta", tetha)

    local phi = -0.202753
    set("sim/flightmodel/position/phi", phi)

    set("sim/flightmodel/position/P", 0)
    set("sim/flightmodel/position/Q", 0)
    set("sim/flightmodel/position/R", 0)


    psi_rad = math.pi / 360 * psi
    tetha_rad = math.pi / 360 * tetha
    phi_rad = math.pi / 360 * phi
    q = dataref_table("sim/flightmodel/position/q")
    q[0] = math.cos(psi_rad) * math.cos(tetha_rad) * math.cos(phi_rad) +
    math.sin(psi_rad) * math.sin(tetha_rad) * math.sin(phi_rad)
    q[1] = math.cos(psi_rad) * math.cos(tetha_rad) * math.sin(phi_rad) -
    math.sin(psi_rad) * math.sin(tetha_rad) * math.cos(phi_rad)
    q[2] = math.cos(psi_rad) * math.sin(tetha_rad) * math.cos(phi_rad) +
    math.sin(psi_rad) * math.cos(tetha_rad) * math.sin(phi_rad)
    q[3] = -math.cos(psi_rad) * math.sin(tetha_rad) * math.sin(phi_rad) +
    math.sin(psi_rad) * math.cos(tetha_rad) * math.cos(phi_rad)

    -- controles neutros
    set("sim/joystick/yoke_heading_ratio", 0)
    set("sim/joystick/yoke_pitch_ratio", 0)
    set("sim/joystick/yoke_roll_ratio", 0)
    --set_array("sim/flightmodel/engine/ENGN_thro_use",MOTOR1,0)

    -- activar fisicas, fin de preparacion
    sleep(0.1)
    set_array("sim/operation/override/override_planepath", 0, 0)

    input_player.play("2.2.csv")
end

proceso = false
do_every_draw("frame()")
function frame()
    if proceso and coroutine.status(proceso) == "suspended" then
        local bien, msg = coroutine.resume(proceso)
        assert(bien, msg)
    end
end

function sleep(s)
    local t1 = get("sim/time/local_time_sec")
    while ((get("sim/time/local_time_sec") - t1) < s) do
        coroutine.yield()
    end
end
